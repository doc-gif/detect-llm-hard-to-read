"""Phase-1 CLI: collect raw per-token data for code complexity research.

This entry point wires together the four extensible layers (language, model,
context, writer). It performs source parsing, LLM inference, isolated
re-inference, and persistence. It does NOT compute research metrics (PPL,
LM-CC, etc.) — that is Phase 2.
"""
from __future__ import annotations

import argparse
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from context import ContextWindow, create_context_strategy
from language import LanguageAdapter, get_adapter_for_path, supported_extensions
from model import ModelAdapter, create_model_adapter
from schema import COLLECTOR_VERSION, CollectionResult, FileMetadata, TokenRecord
from utils.io import read_text
from utils.logging_config import configure_logging, get_logger
from utils.positions import OffsetIndex
from writer import create_writer, supported_formats

LOGGER = get_logger(__name__)


def _build_token_records(
    adapter: LanguageAdapter,
    source: str,
    tokenized,
    full_inference,
) -> Tuple[List[TokenRecord], object]:
    """Create token records enriched with position and AST information.

    Returns:
        A tuple ``(records, tree)`` where ``tree`` is the parsed AST reused
        later for the isolated pass alignment.
    """
    offset_index = OffsetIndex.build(source)
    source_bytes = source.encode("utf-8")
    tree = adapter.parse(source)
    functions = adapter.extract_functions(tree, source_bytes)

    records: List[TokenRecord] = []
    for idx, token_id in enumerate(tokenized.token_ids):
        char_start, char_end = tokenized.offsets[idx]
        is_special = char_start == 0 and char_end == 0

        record = TokenRecord(
            idx=idx,
            token_id=int(token_id),
            token_str=tokenized.token_strs[idx],
            token_metrics={
                "surprisal": full_inference.surprisal[idx],
                "entropy": full_inference.entropy[idx],
                "isolated_surprisal": None,
            },
        )

        if not is_special:
            line, column = offset_index.char_to_line_column(char_start)
            byte_offset = offset_index.char_to_byte(char_start)
            byte_end = offset_index.char_to_byte(char_end)
            token_byte_len = byte_end - byte_offset
            node = adapter.node_at_point(tree, line - 1, column)
            record.line = line
            record.column = column
            record.ast_type = adapter.ast_type(node)
            record.nesting_depth = adapter.nesting_depth(node)
            record.function_id = adapter.function_id_for_point(functions, byte_offset)
            record.is_statement_start = (
                node is not None and adapter.is_statement_start_node(node)
            )
            record.is_function_start = adapter.is_function_start_for_point(
                functions, byte_offset, token_byte_len
            )

        records.append(record)

    return records, (tree, functions)


def _compute_isolated_surprisal(
    model: ModelAdapter,
    source: str,
    records: List[TokenRecord],
    windows: List[ContextWindow],
) -> None:
    """Re-infer each context window in isolation and fill isolated_surprisal.

    Mutates ``records`` in place. Tokens outside any window keep ``None``.
    """
    for window in windows:
        snippet = source[window.char_start : window.char_end]
        if not snippet.strip():
            continue

        local = model.tokenize(snippet)
        local_inf = model.infer(local.token_ids)

        # Map snippet-local token offsets back to global character offsets.
        for local_idx, (ls, le) in enumerate(local.offsets):
            if ls == 0 and le == 0:
                continue
            global_start = window.char_start + ls
            target = _find_record_by_char_start(records, global_start)
            if target is not None:
                target.token_metrics["isolated_surprisal"] = local_inf.surprisal[
                    local_idx
                ]


def _find_record_by_char_start(
    records: List[TokenRecord], global_char_start: int
) -> Optional[TokenRecord]:
    """Best-effort match of a global char start to a token record.

    Note:
        Tokenization of the isolated snippet can differ slightly from the
        full-file tokenization at boundaries. We match on the resolved
        ``column``/``line`` derived char start when possible; here we rely on
        the precomputed mapping built by the caller.
    """
    return _CHAR_START_INDEX.get(global_char_start)


# Module-level index populated per file (kept simple and explicit).
_CHAR_START_INDEX: Dict[int, TokenRecord] = {}


def _index_records_by_char_start(source: str, records: List[TokenRecord]) -> None:
    """Build a char_start -> record index for isolated alignment."""
    _CHAR_START_INDEX.clear()
    offset_index = OffsetIndex.build(source)
    # Reconstruct char_start from (line, column) for non-special tokens.
    line_starts = OffsetIndex.build(source)._line_start_chars  # noqa: SLF001
    for record in records:
        if record.line is None or record.column is None:
            continue
        char_start = line_starts[record.line - 1] + record.column
        _CHAR_START_INDEX[char_start] = record
    del offset_index


def collect(
    source_path: Path,
    model: ModelAdapter,
    context_strategy_name: str,
    project: str,
) -> CollectionResult:
    """Run the full Phase-1 collection pipeline for a single file."""
    LOGGER.info("Reading source: %s", source_path)
    source = read_text(source_path)

    adapter = get_adapter_for_path(source_path)
    LOGGER.info("Selected language adapter: %s", adapter.language_name)

    LOGGER.info("Tokenizing source (%d chars)", len(source))
    tokenized = model.tokenize(source)

    LOGGER.info("Running full-sequence inference (%d tokens)", len(tokenized.token_ids))
    full_inference = model.infer(tokenized.token_ids)

    records, (tree, functions) = _build_token_records(
        adapter, source, tokenized, full_inference
    )
    del tree  # not needed beyond this point

    LOGGER.info("Building isolated context windows: %s", context_strategy_name)
    strategy = create_context_strategy(context_strategy_name)
    windows = strategy.build_windows(source, functions)

    _index_records_by_char_start(source, records)
    LOGGER.info("Running isolated inference over %d windows", len(windows))
    _compute_isolated_surprisal(model, source, records, windows)

    metadata = FileMetadata(
        project=project,
        file=str(source_path),
        language=adapter.language_name,
        model_name=model.model_name,
        model_revision=model.model_revision,
        tokenizer_name=model.tokenizer_name,
        context_strategy=context_strategy_name,
        total_tokens=len(records),
        created_at=datetime.now(timezone.utc).isoformat(),
        collector_version=COLLECTOR_VERSION,
    )
    return CollectionResult(metadata=metadata, tokens=records)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Phase-1 raw data collector for LLM-based code complexity research.",
    )
    parser.add_argument("--model", required=True, help="HuggingFace model id or path.")
    parser.add_argument(
        "--model-revision", default=None, help="Model git revision/commit."
    )
    parser.add_argument(
        "--model-kind",
        default="hf_causal_lm",
        help="Registered model adapter kind (default: hf_causal_lm).",
    )
    parser.add_argument(
        "--source",
        required=True,
        help=f"Source file. Supported extensions: {', '.join(supported_extensions())}",
    )
    parser.add_argument("--output", required=True, help="Output file path.")
    parser.add_argument(
        "--format",
        default="parquet",
        help=f"Output format. Supported: {', '.join(supported_formats())}",
    )
    parser.add_argument(
        "--context-strategy",
        default="function_scope",
        help="Context strategy for isolated_surprisal (default: function_scope).",
    )
    parser.add_argument("--project", default="default", help="Project tag for metadata.")
    parser.add_argument("--device", default=None, help="cuda / cpu (auto if omitted).")
    parser.add_argument(
        "--dtype", default=None, help="float16 / bfloat16 (default: full precision)."
    )
    parser.add_argument(
        "--log-level", default="INFO", help="Logging level (DEBUG/INFO/WARNING)."
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    """CLI entry point."""
    args = parse_args(argv)
    configure_logging(getattr(logging, args.log_level.upper(), logging.INFO))

    import logging as std_logging
    for logger_name in ["__main__", "httpx", "httpcore", "transformers", "huggingface_hub"]:
        std_logging.getLogger(logger_name).setLevel(std_logging.WARNING)

    try:
        source_path = Path(args.source).expanduser().resolve()
        output_path = Path(args.output).expanduser().resolve()

        model = create_model_adapter(
            args.model_kind,
            model_name=args.model,
            revision=args.model_revision,
            device=args.device,
            dtype=args.dtype,
        )
        model.load()

        result = collect(
            source_path=source_path,
            model=model,
            context_strategy_name=args.context_strategy,
            project=args.project,
        )

        writer = create_writer(args.format)
        writer.write(result, output_path)

        LOGGER.info(
            "Done. Collected %d tokens -> %s", result.metadata.total_tokens, output_path
        )
        return 0
    except (FileNotFoundError, ValueError) as exc:
        LOGGER.error("Collection failed: %s", exc)
        return 2
    except Exception:  # noqa: BLE001 - top-level safety net for batch runs
        LOGGER.exception("Unexpected error during collection")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())