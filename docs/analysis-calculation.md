# 分析処理と保存結果の確認

ID結合の上書き、コードの不一致、偏相関のp値、作図する群の不一致を修正した。
保存済みのデータと図は変更していない。
今回の再計算は既存データだけを使った。
モデルの取得、推論、API呼出しは使っていない。

## 確認した実装

`src/analysis/semantic_unit_threshold_analysis.py::load_and_merge_summary` は指標CSVを読む。
回答精度は兄弟の `lm-cc/results` から読む。
対象は `humaneval`、`xcodeeval_apr`、`xcodeeval_code_translation` の3種類である。
各CSVの1,562行から、対象外の6種類594行を除く。
修正前の結合件数は968行である。

`build_frequency_table` はSU数を `[a, b)` の等幅区間へ分ける。
幅は1、5、10である。
各区間の `n` はコードの件数、平均はコードごとの回答精度の単純平均である。
`pass_at_1_std` は標本標準偏差であり、分母は `n - 1` である。
コード1件の区間では標準偏差は欠損になる。
空区間も残し、横軸の上限を最低200にする。
全データを合算した表と、データセット別の表を保存する。
区間内の相関や傾きは計算しない。

`semantic_unit_model_comparison.py::compute_bin_trend` は幅5、10の平均と件数を計算する。
こちらは空区間を落とすため、折れ線はデータがない範囲もまたぐ。
`run_visual_trend_analysis` はp67、p80について図を作る。
3データセット別に加えて、合算した図も作る。
合計16枚である。ファイル先頭には「poolしない」とあるが、実装は合算図も作る。
この合算図をデータセット間の難易度差から独立した結果とは扱わない。

`semantic_unit_model_comparison.py::fit_logistic` は二項ロジスティック回帰ではない。
`curve_fit` で4パラメータ曲線を最小二乗で当てはめる。
目的変数は0〜1の回答精度であり、正解数と試行数は使わない。
上下限パラメータの許容範囲は `[-0.5, 1.5]` である。
したがって、予測値を確率として0〜1に制約していない。
`fit_linear` もコードごとの回答精度を連続値として扱う。

`fit_hinge` はSU数の5〜95百分位の間で境界を300候補試す。
各候補で最小二乗を解き、残差平方和が最小の候補を選ぶ。
境界で連続しており、左右で傾きが変わる。
`fit_step` も同じ候補を探索し、左右2件以上を要求する。
こちらは左右の平均値に段差を許す。
低下方向を強制していない。

`compute_aic_bic` はガウス誤差を仮定した最小二乗のAIC/BICを使う。
分散も推定パラメータとして数える。
二項尤度のAIC/BICではない。
`fit_*_with_dataset` はデータセット別の切片と共通の形を当てはめる。
ロジスティック曲線の場合は共通曲線にデータセット別の差を足す。

## 群相関と回帰線

`src/analysis/util/correlation.py::group_by_metric` は指標で昇順に並べる。
`min_cnt` 件ずつ区切り、回答精度の平均と指標の中央値を作る。
LOCを渡した場合はLOCの中央値も作る。
最後の端数群は一度作るが、`grouped_partial_corr` は相関から除く。
同じ指標値でも別の群へ分かれうる。

`get_grouped_partial_corr` は `floor(N/20)` から `floor(N/8)` まで群サイズを探索する。
有効な群数が9〜11の候補から、Spearman相関の絶対値が最大の候補を選ぶ。
負の相関に限る条件とp値の条件はコメントアウトしてある。
この点は `lm-cc` 側の負の相関だけを選ぶ実装と異なる。
通常のp値は、この探索を考慮していない。
今回、この群選択規則は変更していない。

`correlation_analysis.py::run_analysis` の現行設定はゼロ次相関だけを記録する。
LOCを制御する偏相関の呼出しはコメントアウトしてある。
LM-CCとSU数の間は、群を作らずコードごとのSpearman相関を計算する。
CSV保存もコメントアウトしてあり、通常の実行先は標準出力である。

`plot_analysis_scatter.py` と `plot_analysis_scatter_with_group.py` は偏相関で群サイズを選ぶ。
図の破線は `seaborn.regplot` による群代表点の単純な最小二乗線である。
LOCの影響を除いた偏回帰線ではない。
修正前は相関から除いた端数群も、図の代表点と回帰線に含めていた。
修正後は `include_incomplete=False` で相関と同じ群を描く。
例えば現行p80のAPRでは、SU数の群サイズ29に対して端数10件を除く。
旧スコアを用いた傾きは、端数を含むと約 -0.00105、除くと約 -0.00482 である。
これは主分析の候補を選んだ結果ではなく、描画対象の違いを確かめた値である。

## 修正した結合

5つの入口にあったスコア読込を `src/analysis/score_io.py::load_scores` へまとめた。
修正前はHumanEvalの `__` 以降を落とし、辞書へ代入していた。
同じ基底IDの最後の設問が前の設問を上書きする。
3設問の平均ではない。
`plot_distributions.py` にも同じ上書きがあり、共通の読込へ替えた。
`check_missing_data.py` も完全IDを保ち、指標行のない設問IDを表示する。
修正後は完全なIDを保ち、同じIDの5回平均を結合する。
15回の平均へ変更していない。

HumanEvalのスコア486件のうち、指標CSVにある完全IDは162件である。
派生設問324件は対応する指標行がないため結合しない。
完全IDへ直すだけで162件中17件のスコアが変わる。
その後、コードの不一致4件を除く。
同じ158件で比べると、16件のスコアが変わる。
平均は0.951898734から0.967088608へ変わる。

`audit_humaneval_code` はdetectが計測したソースと基底設問の `main.py` を比べる。
空白とコメントの違いはAST比較で許容する。
意味が同じかどうかを証明する処理ではない。
`HumanEval_1`、`HumanEval_105`、`HumanEval_124`、`HumanEval_150` はASTが異なる。
`HumanEval_1` にはimportの重複という違いがある。
`HumanEval_150` は `else` の所属が異なり、処理の違いも確認した。
4件ともコードの一致を確定できないため、新しい結合から除外する。
過去のコードや指標CSVは書き換えていない。

修正後の件数はHumanEval158件、APR271件、翻訳535件である。
合計は964件である。
翻訳のスコアには、指標CSVにないIDが1件ある。
IDは `0b18f726366147e26db27df379fad323` である。
この1件も、従来どおり結合しない。

nested形式で `pass@1` が欠けた場合は、0ではなく欠損として除外する。
現行の保存スコアでは、この欠損は0件だった。
重複したJSONキー、範囲外のスコア、キーと `task_id` の不一致はエラーにする。
指標CSVの `(dataset, uid)` の重複と欠損もエラーにする。
現行p67、p80の各1,562行に、このキーの重複はない。

## 偏相関のp値と小さな実行不具合

Macの既存環境は `pingouin 0.6.1` である。
この版のp値列は `p_val` だが、既存コードは `p-val` を読んでいた。
そのため、偏相関の処理は代替計算へ入っていた。
代替計算は順位の回帰残差へPearson相関を適用する。
そのp値を使うと自由度が `n - 2` になり、共変量1本の推定を数えない。

修正後は `p_val` と `p-val` の両方を読める。
代替計算のp値は、共変量1本を考慮した自由度 `n - 3` で求める。
小さな6件の例で、通常の計算と代替計算のrとp値が一致した。
群サイズ探索後のp値を主張に使えるようにする変更ではない。
LOCで調整した順位残差が一定なら、偏相関は未定義として返す。
LOCの順位が一定の場合と、3群以下の場合も未定義として返す。
これにより、rank不足の行列から返る値を候補選択に使わない。
共分散行列のrank不足に関する警告は、監査CSVの件数に残してある。
翻訳のLM-CCと精度の偏相関は、LOCを制御すると全候補で未定義だった。
この組合せを `undefined_combinations.json` に記録した。

`compare_models` はstepモデルを推定できないときの `None` を除く。
AIC差の分岐は、常に0になる最良モデルの差ではなく2位との差を見る。
表示する最良モデルはAICで選ぶため、「AIC/BIC最良」という表示も直した。
`build_frequency_table` は任意列のLM-CCがなくても動く。

## 保存CSVと現行コードの照合

`results/semantic_unit_binning/analysis_summary_p80_with_score.csv` は968行ある。
これを入力にして、保存された区間表12件を再計算した。
件数、平均、標準偏差、LM-CC平均は12件すべてで一致した。
同じ入力からモデル比較22行も再計算した。
RSS、AIC、BICは22行すべてで一致した。
最大の絶対誤差はRSSで約1.4e-14、AIC/BICで約2.3e-13である。

ただし、この保存mergedと現行p80 summaryは同じ指標値ではない。
968行中、SU数が346行、LM-CCが291行で異なる。
LOC、PPL、トークン数は一致する。
したがって、保存表を「現行p80 summaryから作った表」とは説明できない。
旧mergedのSU/LM-CCは `fbfc5c3` のp80 summaryと968行すべて一致した。
保存mergedは閾値1.2515で再計算すると、968行すべてのSU数とLM-CCが一致する。
現行p80 summaryは閾値1.3238に対応する。
同じp80という名前でも、数値の閾値が異なる。
現在の指標と旧mergedを混ぜて分析しない。

`run_model_comparison` は修正前、保存mergedがあればそれを優先した。
修正後はsummaryとスコアから毎回結合し直す。
修正したID結合を、古いキャッシュが打ち消すことを防ぐ。

## 図と実行履歴から分かる範囲

保存図の名前は、対応する作図関数の出力名と一致する。
区間図は `plot_frequency_table`、モデル図は `plot_model_comparison` が候補である。
データセット制御の図は `plot_dataset_controlled_comparison` が候補である。
トレンド図は `plot_visual_trend` が候補である。

Gitには次の記録がある。

- `e28e9cc` は2026年7月9日に区間分析とモデル比較を追加した。
- `fbfc5c3` は2026年7月10日にモデル比較と区間表を変更した。
- `12c12a9` は2026年7月12日にトレンド図16枚と関連実装を保存した。
- `1c64253` は2026年7月26日に区間図の幅を揃える変更と表を保存した。
- `2476ee6` は2026年7月27日に散布図を更新した。

Gitの保存時刻は実験の実行時刻ではない。
`batch.log` と `inference.log` から、これらの分析を実行したコマンドは確認できなかった。
保存PNGの画素がどのコード版と入力から生まれたかは未確認である。
`model_comparison_dataset_controlled.png` は現在の出力名と異なる旧図である。
この図を現在の再計算結果として使わない。
CSVの数値再現とPNGの生成記録は区別する。

今回、修正後のトレンド図16枚を別の新規ディレクトリへ作った。
作成先は `results/audit/2026-10-19-visual-checked/figures/` である。
HumanEvalのp80・幅5の図を開き、軸と描画を確認した。
これは既存の可視化を再計算したものであり、新しい主分析ではない。

## 再現手順

リポジトリ直下で、既存の `.venv` を使う。
出力先には、まだ存在しないディレクトリを指定する。

```sh
MPLBACKEND=Agg MPLCONFIGDIR=/tmp/codex-mpl PYTHONDONTWRITEBYTECODE=1 .venv/bin/python scripts/audit_saved_analysis.py --output-dir results/audit/recheck-001
MPLBACKEND=Agg MPLCONFIGDIR=/tmp/codex-mpl PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:src .venv/bin/python -m unittest discover -s tests -p test_analysis_integrity.py
MPLBACKEND=Agg MPLCONFIGDIR=/tmp/codex-mpl PYTHONDONTWRITEBYTECODE=1 .venv/bin/python src/analysis/semantic_unit_model_comparison.py --mode visual --output-dir results/audit/visual-001
```

`--mode models` は既存の最小二乗モデル比較を再計算する。
二項ロジスティック回帰は実装していない。
区間表と棒グラフには `semantic_unit_threshold_analysis.py` を使う。
同じ `--output-dir` と、任意の `--summary` を指定できる。
主要な作図入口は、指定しなければ日時と乱数を付けた新規ディレクトリへ保存する。
既存の出力先は上書きせず、エラーにする。

今回の最終監査結果は `results/audit/2026-10-19-analysis-final/` にある。
`audit_report.json` に入力ファイルのSHA256と数値照合を保存した。
`corrected_join_p67.csv` と `corrected_join_p80.csv` は修正後の結合結果である。
`corrected_bins_p67/` と `corrected_bins_p80/` は修正後の区間表である。
`score_join_comparison.csv` は修正前後のスコアと採否を示す。
`unmatched_score_ids.csv` は指標行のない設問IDを示す。
`code_identity_p67.csv` と `code_identity_p80.csv` はコード照合を示す。
`legacy_group_search_and_plot_tail.csv` は既存の探索規則と端数の影響を示す。
ここにあるp値は、群数探索後の名目上の値である。

テストは17件成功、0件失敗だった。
修正後のトレンド図は16枚生成した。
元データ、過去のCSV、過去のPNGは上書きしていない。
