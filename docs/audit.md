# 調査結果と再現手順

結合ミス、p80の閾値の記載違い、偏相関と作図の不一致を修正した。元データと過去の出力は保持した。新しい主分析やSU抽出規則は採用していない。

## 修正した問題

1. HumanEvalの派生IDを落とす処理が、平均を取らずに最後の値で上書きしていた。両リポジトリで完全IDを使うようにした。欠損スコアを0にする処理を止め、重複IDも検出する。
2. detectの測定コードは4件で基本IDの設問コードとASTが異なった。`HumanEval_1`、`105`、`124`、`150`を新しい結合から除き、理由を記録した。単なる空白・コメントの差は除外しない。
3. 同じp80という名前で、二つの閾値を使っていた。現在のsummaryは1.3238、古い結合済みCSVは1.2515で再現する。実験スクリプトは保存summaryに対応する1.3238を使うようにした。
4. モデル比較は古い結合済みCSVを無条件で使っていた。現在のsummaryとスコアから再結合するようにした。以前のCSVを自動で修正後の入力にしない。
5. 群の相関は端数群を除くが、散布図の回帰線には端数群を含めていた。回帰線も相関と同じ群を使うようにした。回帰線はLOC調整後の線ではなく、代表点への最小二乗直線である。
6. detectでは`pingouin`のp値列名の違いで例外処理に入り、共変量を考慮しない自由度でp値を求めていた。列名の両形式に対応し、共変量が1本なら自由度を`群数−3`にした。順位の残差が一定で偏相関を定義できない候補も除く。
7. 前処理で`print`と`else`が消える例を確認した。docstring以外のASTが変わる場合は、推論前に停止するチェックを加えた。保存済みのentropyは別コード用に読み替えず、保持する。
8. 保存木の出力処理には、存在しないimport先、戻り値の個数違い、改行の二重挿入があった。現helperに合わせ、再出力先を分けた。SU抽出の計算規則は維持した。

lm-cc側のHumanEvalは、LOCも基本設問と同じコードから数えるようにした。非空行数という定義を保ち、162値中9値が変わる。APRと翻訳のLOCは、回答入力と全件一致した従来の値を使う。

HumanEvalの5回の集計には、欠損・重複・正誤の矛盾を検出するチェックも加えた。既存の486設問では、各設問に5回の判定があり、保存平均はすべて正解数÷5と一致した。集計の分母が今回の保存値を壊していたわけではない。

## 修正前後の数値

| 確認対象 | 結果 |
| --- | --- |
| HumanEvalの完全IDへの変更 | 162行のうち17行で、上書きされたスコアから基本設問のスコアへ変わる。 |
| detectのコード一致を確認した158行 | 同じ158行で比較すると16行が変わる。平均は0.951898734から0.967088608となる。 |
| detectの修正後の結合 | HumanEval158、APR271、翻訳535の計964行となる。p67とp80の両方で同じ件数である。 |
| lm-ccの保存LM-CC | 6データセットの1,185値を保存entropyと閾値0.67から再計算し、すべて一致した。旧保存木とも一致した。 |
| 20個の保存summary | それぞれ対応する数値閾値で、SU・LM-CC・LOCが各31,240値すべて一致した。 |
| 旧結合済みCSVのSU・LM-CC | 保存Parquetと1.2515から968行すべて再現した。 |
| 保存された区間表 | 旧結合済みCSVから12表すべて一致した。 |
| 保存されたモデル比較 | 旧結合済みCSVから22モデルのRSS・AIC・BICが一致した。最大誤差は約2.3×10⁻¹³だった。 |

lm-ccの旧群探索を残した再計算では、HumanEvalの偏相関は`r=−0.0555, p=0.8790`となった。翻訳には条件を満たす負の偏相関が残らなかった。両課題の旧図は、修正後の偏相関を示す図として使えない。これらも探索後の値であり、新しい主分析の結果ではない。

平均値の変化は結合修正の影響であり、モデル性能が改善した結果ではない。修正前の162行と、除外後の158行をそのまま比較してはならない。

基本設問への結合では、HumanEvalの派生設問324件を使わない。これは5回平均を保つための今回の範囲である。3設問をまとめた15回の平均は別の分析になる。派生設問のコードが違う例もあるため、無条件に足せない。

テストはdetectで21件成功、lm-ccで22件成功、失敗は0件だった。合計43件である。[実行コマンド](evidence/tests.json)と[修正後のコードのSHA-256](evidence/revised-source-files.json)を記録した。

## 保存ファイルと実行記録

[145個のCSV・PNGの一覧](evidence/artifact-inventory.csv)に、パス、SHA-256、生成候補、最後のGitコミットを記録した。候補の関数を特定できても、実行時のコマンドや環境が確認できたとは扱わない。表の数値の再現と、PNGを当時と同じ条件で生成したことも区別する。

`detect/scripts/batch.log`には1563件を対象にし、成功扱い1562件、失敗1件とある。成功件数は既存ファイルのスキップを含む。翻訳コード`0b18f726366147e26db27df379fad323`はメモリ不足で失敗した。コード536件に対して保存Parquetが535件であることと整合する。ログの日付は6月15日で、現Parquetのメタデータより古い。このログだけで、現在の保存ファイルを作った実行回までは確定できない。

original3課題の968コードは、内容ハッシュがすべて異なった。ASTを解析できた966件も、課題内・課題間で重複がなかった。APRの2件は字下げエラーでASTを解析できなかった。近似コードや意味の同一性は調べていない。

現在のParquetのトークン列は、全1562件で現在の入力コードに対応した。保存メタデータはUTCで6月19〜20日の測定を示す。日本時間では6月19日17:21〜6月21日01:13である。ただしモデルのrevisionを記録していない。今回、モデル推論自体は再実行していない。

保存木1562件は、木のJSON内部の旧entropyと閾値0.67から再現する。現Parquetとはentropyが全件異なるため、現在のSU表の生成元とは扱わない。無印`analysis_summary.csv`はSUとLM-CCがp10の表と一致した。

## 再現手順

detectの再計算には既存のdetectの`.venv`を使う。今回の分析用環境はPython 3.13.9、NumPy 2.4.6、pandas 3.0.3、SciPy 1.17.1だった。環境の再インストールやモデルの読み込みは不要である。

出力先は存在しないディレクトリを指定する。以下の名前を使用済みなら、新しい名前へ変える。

```sh
cd /Users/hyoishitobi/PycharmProjects/detect-llm-hard-to-read
PYTHONPATH=.:src:src/analysis PYTHONDONTWRITEBYTECODE=1 MPLBACKEND=Agg MPLCONFIGDIR=/tmp/codex-mpl .venv/bin/python -m unittest discover -s tests
.venv/bin/python scripts/audit_saved_semantic_metrics.py --output-dir results/audit/new-semantic-check
MPLBACKEND=Agg MPLCONFIGDIR=/tmp/codex-mpl .venv/bin/python scripts/audit_saved_analysis.py --output-dir results/audit/new-analysis-check
```

```sh
cd /Users/hyoishitobi/PycharmProjects/lm-cc
MPLBACKEND=Agg MPLCONFIGDIR=/tmp/lmcc-mpl-cache PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests
.venv/bin/python scripts/audit_saved_calculations.py --output-dir out/audit/new-score-check --with-correlations
.venv/bin/python scripts/audit_saved_lmcc_metrics.py --output-dir out/audit/new-lmcc-check
```

lm-ccの再計算にはlm-ccの`.venv`を使った。LM-CCの再計算ではモデルを生成せず、保存トークン値だけを使う。[1,185件の比較記録](evidence/lmcc-metric-verification.json)を保存した。pingouinはlm-ccが0.5.5、detectが0.6.1である。両方のp値列名を受け付けるよう修正した。

今回の修正後の結合表と区間表は、detectの`results/audit/2026-10-19-analysis-final/`に保存した。`score_join_comparison.csv`は新旧スコアを同じIDで比較する。`code_identity_p67.csv`と`code_identity_p80.csv`はコードの一致とハッシュを示す。`unmatched_score_ids.csv`は指標に結合しなかったスコアIDを残す。

`corrected_join_p67.csv`と`corrected_join_p80.csv`が修正後の964行である。各閾値の`corrected_bins_*`に幅1・5・10の表を残した。`legacy_group_search_and_plot_tail.csv`は群数探索と端数除外の影響を示す。ここでのp値は過去の探索方法を保った値であり、新しい主分析の検定結果ではない。翻訳のLM-CCと精度のLOC調整では、有効な候補が残らなかった。未定義の組合せは`undefined_combinations.json`に残した。

初回診断用の`2026-10-19-analysis/`と、途中の`2026-10-19-analysis-checked/`も残っている。偏相関の修正途中の記録である。修正後の結果には`2026-10-19-analysis-final/`を使う。

## 残る未確認事項と方法上の制約

- PNGの元の実行コマンド、依存関係、描画環境は未確認である。`lmcc_distribution_comparison.png`の生成処理も特定できていない。既存画像を修正済みの図とは呼ばない。
- 閾値1.3238をどのトークン集合から求めたかは未確認である。保存値を再現する閾値であることは確認した。現在のoriginal3課題の80パーセンタイルは約1.2515である。
- SU helperは改行以外のバイト表記を復元しない。109ファイルで元コードと木を作る文字列に差が生じる。この制約を直すと指標の定義と過去の値が変わるため、今回の結合修正とは分けた。
- `lm-cc`側にも前処理後の指標コードと回答入力コードの差がある。詳細と対象件数は[回答と指標の調査](score-calculation.md)を参照する。全件の意味が同じとは確認していない。
- 9〜11群から最大相関を選ぶ処理、複数閾値の探索、hinge・stepの境界探索は残っている。選択後の通常のp値や、同じデータで比較した当てはまりだけで説明力を断定しない。
- 旧結果の回答を、当時のモデル・設定で再生成できるかは未確認である。今回は保存された採点値と計算経路を調べた。

[保存済みデータのハッシュ照合](evidence/preservation-check.json)では、lm-ccの6,578ファイルとdetectの6,392ファイルに変更はなかった。開始時の未コミット画像も保持した。

各問題のファイル名・関数名・最小例は、[SUの計算](su-calculation.md)、[回答の計算](score-calculation.md)、[結合と分析](analysis-calculation.md)にまとめた。[今後の分析案](analysis-plan.md)は、これらの修正とは別の提案である。
