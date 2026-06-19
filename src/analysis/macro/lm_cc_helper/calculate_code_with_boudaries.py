def get_code_with_boundaries(tokens, entropies, threshold=0.67):
    clean_code_lines = []
    start_end_tokens = []
    current_line = ""
    line_start_token = 0
    text = ""
    should_divide = False
    for idx, (token, entropy) in enumerate(zip(tokens, entropies)):
        # code llama
        token = token.replace("<0x0A>", "\n").replace("\u2581", " ")
        # print((token, entropy))
        last_entropy = 0 if idx == 0 else entropies[idx - 1]

        if idx > 0 and entropy >= threshold:
            should_divide = True

        current_line += token
        if "\n" in token or idx == len(tokens) - 1:
            clean_code_lines.append(current_line)
            current_line = ""
            start_end_tokens.append((line_start_token, idx))
            line_start_token = idx + 1
            if should_divide:
                last_newline_pos = text.rfind('\n')
                text = text[:last_newline_pos + 1] + "\n" + "=" * 30 + "\n" + text[last_newline_pos + 1:]
                should_divide = False
        text += token
    if line_start_token < len(tokens):
        start_end_tokens.append((line_start_token, len(tokens) - 1))

    return text, clean_code_lines, start_end_tokens