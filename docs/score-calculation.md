# 採点、ID結合、LM-CCの相関を確認した結果

HumanEvalの5回平均は保存した採点記録と一致した。一方、本人が追加した相関処理は派生IDを落とし、別の設問の値で上書きしていた。完全IDで結合するように直した。以下のファイル名は、特記しない限り `lm-cc/` からの相対パスである。

## リポジトリの役割と調査時の状態

`lm-cc` は先行研究を基にした実験用リポジトリである。データセット、回答、採点結果、トークンのエントロピー、木を保存している。本人が追加した再計算と描画の入口もある。変更のない先行研究クローンではない。

調査時のHEADは `96dd50f384240a2f75c377b9a109baee8d1d099d` だった。remoteは `https://github.com/doc-gif/lm-cc.git` である。既存の `AGENTS.md` は対象内にも親ディレクトリにも見つからなかった。

`9d0f6a2` は2026年6月20日に、エントロピーからLM-CCを再計算する処理を追加した。同じコミットに、LOCの生成、相関計算、分布の比較がある。`96dd50f` は翌日に散布図の処理と3枚の画像を追加した。

作業開始時に `scripts/plot_lmcc_scatter.py` と3枚の散布図が未コミットだった。コードの差分は `plt.xlim(right=850)` の追加だった。この差分と既存の画像を保持した。未追跡のデータ、LOC、画像も保持した。

コミットの日付は実行日を証明しない。今回確認した3枚の散布図には実行ログがない。図の数値と旧処理の再計算値は一致したが、生成時のコマンドと環境は未確認である。

`out/lmcc_paired_comparison.png` に対応する保存先は `compare_lmcc_distributions.py::main()` にある。IDが共通する原形とsimplifiedのLM-CCを比較し、HumanEvalを描く処理である。この保存画像の実行記録は未確認である。`out/lmcc_distribution_comparison.png` は、現行スクリプト内に対応する保存先が見つからなかった。生成元は未確認である。

## HumanEvalの採点と5回平均

`scripts/execution_reasoning.sh` は `tasks/ier/ier.py` を試行番号1〜5で呼ぶ。その後、`tasks/ier/parse_result.py` と `tasks/ier/get_scores.py` を呼ぶ。スクリプトに書かれたモデルは `deepseek-v3` である。この記述だけでは、保存結果を生成したモデルを確定できない。

`parse_result.py` の `parse_chatgpt()` は回答中の `<<<Output>>>` と `[END-OF-RESPONSE]` を使う。`get_result()` は予測と `dataset/humaneval/<完全ID>/output.txt` を比較する。次の処理を経た文字列が一致すれば正解である。

- 改行と半角空白を除く。
- 二重引用符を一重引用符へ変える。
- 文字列の先頭と末尾にある引用符かバッククォートを1文字ずつ除く。
- 予測に残った `[END-OF-RESPONSE]` を除く。

同名の `compare_string_answers()` もあるが、`get_result()` は使っていない。正解ラベルを作る処理は、一般的なPython値の比較ではない。たとえば文字列中の空白も消える。採点規則を変更すると研究上の正解の定義が変わるため、今回は変更しなかった。

`get_result()` は正解ファイルか予測ファイルがない設問を飛ばす。旧 `calculate_pass_at_k()` は5個の結果ファイルの和集合を集計した。一部の試行にないIDも、分母を5として計算していた。今回、試行間でIDが違う場合はエラーにした。重複、正誤の矛盾、空の試行もエラーにした。全5試行から消えた設問は、このファイル群だけでは検出できない。

`calculate_pass_at_k()` の式は `1 − C(n−c,k)/C(n,k)` である。`k=1` なら `c/n` となる。5回中3回正解は `0.6` である。今回、CLIの `--k` を無視していた処理も直した。研究の5回平均には `--k 1` を使う。

保存データの確認結果は次のとおりである。

- `results/humaneval-ier/initial-output/result-humaneval-1.json` から `-5.json` には、毎回486件の採点がある。正解数は順に456、459、463、457、458件である。重複、正誤の矛盾、試行間の欠損はない。
- `results/humaneval-ier/results_score.json` の486値は、各完全IDの正解数を5で割った値と一致する。
- simplifiedの5ファイルには、毎回180件の採点がある。正解数は171、170、171、171、172件である。`results_score_simplified.json` の180値も再計算と一致する。
- 予測文字列と元の応答ファイルは、今回確認したHumanEvalの結果ディレクトリにない。そのため、保存ラベルの集計は確認したが、回答からの再採点は未確認である。

## APRとCode Translationの採点

`tasks/evaluate_apr.py` は `bug_code_uid` を設問IDに使う。各回答から最初のPythonコードブロックを抜き、隠しテストをすべて通れば、その回答を正解とする。タイムアウトと実行エラーは不正解になる。`pass@1` は正解回答数を実際の `choices` 数で割った値である。隠しテストの通過率の平均 `avg_pass_rate` とは異なる。

`tasks/evaluate_ct.py` は `code_uid` を使う。Cコードをコンパイルして隠しテストを実行する。コンパイル失敗、タイムアウト、捕捉した実行例外は不正解になる。すべてのテストで標準出力が一致すれば、その回答を正解とする。終了コードが非0でも出力だけで通す経路は残っている。今回保存されていた詳細には、この条件で正解になった例はなかった。

両処理とも試行数は `len(choices)` である。コード上で5に固定してはいない。テストが0件なら成功と扱う経路もある。CTは設問全体の評価で例外が起きると、結果からその設問を除く。これらの処理を今回まとめて書き換えてはいない。

保存データの確認結果は次のとおりである。

- 原形APRの271設問とCTの536設問には、すべて5回答が保存されている。回答ファイルのIDとスコアのIDは一致する。重複IDはない。
- 原形APRとCTには、各回答の採点詳細が保存されていない。`pass@1` はすべて0.2刻みだが、各値の正解数は独立に確認できない。元の生成コードは今回再実行していない。
- simplified APRの58設問とCTの99設問には、5回答と採点詳細がある。全157設問で `pass_cnt/sample_cnt` と保存 `pass@1` が一致する。空のテストはない。
- simplifiedの計785回答で、保存した各テストの正誤、通過数、回答の正誤、設問の正解数が一致する。確認した隠しテストの延べ数はAPRが16,975件、CTが36,240件である。これは保存記録の整合確認であり、再実行による確認ではない。

## ID結合の修正

HumanEvalの486設問は、162の基底IDに3入力ずつ対応する。末尾なし、`__0`、`__1` は試行番号ではなく、入力の異なる設問である。各完全IDに5回平均がある。

旧処理は末尾を落として辞書へ代入していた。該当するのは `run_lmcc_correlation.py` と `plot_lmcc_scatter.py` の `load_scores()` である。平均処理はなく、JSON内で最後に現れた設問の値が残った。3設問のスコアが異なる基底IDは36件あった。

今回、`scripts/utils/score_io.py::load_scores()` に完全IDを保つ読み込みを追加した。2つの入口で共用する。欠損した `pass@1` を0に変える処理もやめた。JSONの重複キー、IDの矛盾、非数値、範囲外の値はエラーにする。

本人が再計算したHumanEvalのLM-CCは、基底ID162件を持つ。これを同じ完全IDのスコアと結ぶ。派生324設問は未結合として監査結果へ出す。3設問15回答の平均には変えていない。162行中17行のスコアが変わる。平均は旧処理の `0.949382716` から `0.967901235` になる。例として `HumanEval_36` は旧処理が `0.0`、完全IDで読むと `1.0` である。

3入力をまとめることは、別の分析単位を選ぶ判断である。採用する場合は3入力の重みと欠損規則を決める。同じコードへの回答を15本の独立したコードと数えてはならない。

CTの保存スコアは536件だが、本人が再計算したLM-CCは535件である。未結合IDは `0b18f726366147e26db27df379fad323` である。除外が発生した時点と実行ログは未確認である。

## コードの一致とLOC

LOCの規則は `scripts/utils/metrics.py::get_code_loc()` の非空行数である。空白だけの行を除く。コメントとdocstringの行は数える。

HumanEvalの `results/humaneval-ier/entropy/entropies-CodeLlama-7b-hf-1.0.json` は162件である。全162件の `code` が基底設問の `dataset/humaneval/<完全ID>/main.py` と文字列まで一致した。このエントロピーが本人の `calc_lmcc_from_entropy.py` の入力である。

旧LOCは `generate_loc_data.py` が兄弟の `detect-llm-hard-to-read/data` から作っていた。HumanEvalの抽出は、同じ基底IDで最初に見つけたコードを採用していた。基底設問とASTが異なるコードが4件あった。該当するのは `HumanEval_1`、`105`、`124`、`150` である。

今回、HumanEvalのLOCだけを、基底設問と一致した保存 `code` から求めるようにした。非空行数の定義は変えていない。コードの書式の差も含め、162値中9値が変わる。ASTの差4件とLOCの差9件は別の数である。後者のIDは `145`、`87`、`83`、`128`、`51`、`75`、`134`、`1`、`151` である。元の `loc.json` は変更していない。

APRの271件とCTの535件では、旧LOCが回答時の入力コードの非空行数と全件一致した。こちらはLOCの出典も値も維持した。エントロピーの `code` は前処理後なので、そこからLOCを数えると別の定義になる。前処理後のLOCとの差はAPRで182件、CTで185件あった。この差だけでは旧LOCの不具合と判断できない。

保存したHumanEvalの `block_trees-...-thres-0.67.json` は486件である。`scripts/utils/entropy.py::entropy()` が基底の木とコードを派生2件にも複製する。そのため、全162群で木の `code` が3件とも一致する。一方、実設問の `main.py` は5群でASTが異なり、派生9件で保存した木のコードと一致しない。本人の基底162件のLM-CCと、先行経路の486件の木を区別する必要がある。

## 前処理と回答コードの不一致は残る

`scripts/utils/entropy.py::entropy()` はAPRでコメント除去後に整形する。CTでは整形後にコメントを除く。`scripts/utils/utils.py` の正規表現による削除と、Blackの `--fast` を使う整形が関係する。

保存した前処理後のコードを、回答ファイルの入力コードとASTで比較した。APRは271件中224件が一致し、45件が不一致、2件は構文解析に失敗した。CTは535件中520件が一致し、14件が不一致、1件は構文解析に失敗した。ASTの不一致には前処理で除いたdocstringも含み得る。全件を意味の変化と断定はしない。docstringだけを除いて比較すると、APRは250件一致、19件不一致、2件解析失敗だった。CTは529件一致、5件不一致、1件解析失敗だった。

ただしCTの `0b89808a1534e5dd349fcd06e195071f` では、意味のある差を確認した。回答側には `if b == 0` の分岐で出力し、`else` で別処理をするコードがある。保存したエントロピー側では出力と `else` が消え、後者の処理が `if b == 0` の中にある。現在の前処理をこの1件へ適用すると、保存コードと文字列まで一致した。モデルは使っていない。

最小例でも問題を再現した。`if/else` の各分岐に、`user's` を含むコメントを置く。正規表現が2つのアポストロフィ間を文字列と扱い、出力文と `else` を消していた。

`utils/code_integrity.py::assert_preserved_program()` を追加した。docstringを除いたASTが一致しない場合、`utils/entropy.py` は推論前に例外で停止する。構文解析に失敗した場合も停止する。コメントやdocstringの除去は許可するが、文字列の値や分岐の変更は許可しない。

保存されたトークンのエントロピーを、別のコード用に読み替えて救済することはできない。今回はモデルを再実行していない。正規表現を新しい抽出規則へ置き換えてはいない。代わりに、前処理で実処理が変わったら計測前に停止するガードを追加した。原形XcodeEvalのLM-CCと回答精度の関係は、この不一致の制約付きで扱う。新しい主分析には、コードの一致を確認した範囲を使う判断が必要である。

## 群、相関、偏相関、回帰線

以下は現行の本人の実装であり、論文の定義を引用した説明ではない。

`scripts/utils/correlation.py::group_by_metric()` はLM-CCの昇順で並べる。`min_cnt` 件ごとに区切り、精度の平均、LM-CCの中央値、LOCの中央値を求める。幅を固定したSU区間ではない。同じLM-CC値も別の群に分かれ得る。

`grouped_partial_corr()` は最後の群が `min_cnt` に満たなければ除く。単相関は群の代表値のSpearman相関である。偏相関は群のLOC中央値を調整するSpearman偏相関である。個々のコードの相関をそのまま推定しているわけではない。

`get_grouped_partial_corr()` は `floor(N/20)` から `floor(N/8)` まで群の件数を探索する。9〜11個の完全な群ができ、負の相関となる候補だけを残す。その中で絶対値が最大の相関を選ぶ。`p < 0.05` の条件はコメントアウトされている。フィルターを撤廃したという旧コメントは、実処理と一致していなかったので直した。探索規則自体は今回は変更していない。

この探索で選んだp値は、候補を試した回数を調整していない。新しい主分析の有意性を示すp値として使わない。教授の区間評価は、SUの範囲内で精度との関係を確かめるものである。この全体の群平均の相関とは目的が異なる。

`plot_lmcc_scatter.py::plot_scatter()` の線は `seaborn.regplot()` の最小二乗直線である。群のLM-CC中央値と精度平均を使い、LOCは調整しない。図に示す偏相関係数とは別の計算なので、凡例に `unadjusted OLS` と明記した。

旧描画処理は相関から除いた端数群も線に使っていた。今回、相関と同じ群だけを描くように直した。旧APRでは271件を27件ずつ区切り、相関は10群だったが、図には最後の1件もあった。旧CTでは535件を59件ずつ区切り、相関は9群だったが、図には最後の4件もあった。保存画像でも、この余分な代表点を確認した。

偏相関の例外処理にも修正を加えた。順位の残差へ通常のPearson検定を使うと、自由度が `n−2` になる。LOCを1変数調整したp値は `n−3` とした。pingouinの `p-val` と `p_val` の両列名にも対応した。このMacのlm-cc環境はpingouin 0.5.5であり、旧列名が有効だった。

さらに、LOCの順位でLM-CCか精度の順位を説明し切ると、偏相関は未定義になる。この場合もpingouinの擬似逆行列が数値を返していた。今回、順位の残差が一定なら未定義として候補から除くガードを追加した。LOCの順位が一定の場合と、4群未満の場合も除く。

## 保存画像との照合と修正後の再計算

旧 `out/plots/scatter_partial_*.png` の表示値は、旧結合と旧LOCで再計算した値と丸め桁まで一致した。HumanEvalは `r=−0.654, p=0.079`、APRは `r=−0.831, p=0.005`、CTは `r=−0.967, p<0.001` である。

修正後も過去の群探索を残して再計算した。HumanEvalは11群で `r=−0.055467838, p=0.879036728` となる。162件を14件ずつ区切り、最後の8件を除く。APRは10群で `r=−0.831285544, p=0.005484010` となる。CTには条件を満たす負の偏相関の候補が残らない。これは不具合修正の影響を確認する計算であり、主分析の提案ではない。有意になったことを、修正や分析方法の正当化に使わない。

修正後のHumanEvalとAPRの2枚の図は別ディレクトリに生成した。CTは有効な偏相関の候補がないため、描画を省略した。既存のスコアJSON、LOC、図は上書きしていない。図の保存先は `--output-dir` で指定し、同名ファイルがあれば拒否する。スコア保存も既存ファイルを拒否する。

## 再現手順

`lm-cc` のルートで、既存の仮想環境を使う。以下の出力先は未作成の名前へ変える。モデルやAPIは使わない。

```sh
MPLBACKEND=Agg MPLCONFIGDIR=/tmp/lmcc-mpl-cache PYTHONDONTWRITEBYTECODE=1 \
  .venv/bin/python -m unittest discover -s tests -v

MPLBACKEND=Agg MPLCONFIGDIR=/tmp/lmcc-mpl-cache PYTHONDONTWRITEBYTECODE=1 \
  .venv/bin/python scripts/audit_saved_calculations.py \
  --output-dir /tmp/lmcc-audit-20261019-new --with-correlations

MPLBACKEND=Agg MPLCONFIGDIR=/tmp/lmcc-mpl-cache PYTHONDONTWRITEBYTECODE=1 \
  .venv/bin/python scripts/plot_lmcc_scatter.py \
  --output-dir /tmp/lmcc-plots-20261019-new

PYTHONDONTWRITEBYTECODE=1 python3 scripts/tasks/ier/get_scores.py \
  --k 1 --output-dir results/humaneval-ier --dataset humaneval \
  --output-file /tmp/humaneval-score-20261019-new.json
```

テストは22件成功、0件失敗である。保存データの監査と2枚の図の生成も成功した。MacのGUIバックエンドでは描画が異常終了したため、上記の `MPLBACKEND=Agg` を指定した。

`audit_saved_calculations.py` は `summary.json` と3つの結合CSVを新規作成する。JSONには入力のSHA-256、HEAD、試行数、未結合ID、修正前後の値を保存する。旧統計処理は `96dd50f` の3関数を読み、旧入力と組み合わせて再現する。採点やモデルを呼ぶ旧処理は実行しない。前処理後のコードと回答コードの比較結果も保存する。CSVの `legacy_score` は旧上書き処理の値、`exact_id_score` は完全IDの値である。`saved_loc` は旧保存値、`corrected_loc` は今回使う値である。`entropy_source_loc` は前処理後との比較用であり、XcodeEvalの新しいLOC定義ではない。

今回の最終監査結果は[監査の記録](evidence/lmcc-verification/summary.json)にある。修正後の図は`evidence/lmcc-plots/`に置いた。検討途中の出力はこの記録に含めていない。

## 保存LM-CCの再計算

`out/lm_cc/` の6データセット、1185件を保存entropyから再計算した。`scripts/lm_cc/lm_cc.py` の `get_code_with_boundaries()` に閾値0.67を渡した。続いて `CodeBlockProcessor.parse_code_blocks()` と `get_lmcc()` を使った。

再計算値は1185件すべて保存LM-CCと一致した。HumanEvalは162件、simplifiedは60件だった。APRは271件、simplified APRは58件だった。翻訳は535件、simplified翻訳は99件だった。入力・出力IDに重複、欠損、余分なIDはなく、計算エラーもなかった。

旧 `block_trees-CodeLlama-7b-hf-1.0-thres-0.67.json` も完全IDで照合した。対応する1185件で、木の構造、tokens、entropyが一致した。旧木へ同じ式を適用したLM-CCも全件一致した。HumanEvalの木には派生IDのコピーが含まれるが、この比較には入力entropyと同じ基底IDだけを使った。

再現には`lm-cc/scripts/audit_saved_lmcc_metrics.py`を使う。実行にはlm-ccの既存Python 3.11.9環境を使った。`HF_HUB_OFFLINE=1` と `TRANSFORMERS_OFFLINE=1` を指定した。モデルのクラスは生成せず、保存トークン値だけを使った。入力JSON、保存LM-CC、旧木、計算コードのSHA-256と全件の比較値を [比較記録](evidence/lmcc-metric-verification.json) に記録した。これは保存値の再現であり、前処理後のコードと回答入力コードが同じ意味であることを保証しない。
