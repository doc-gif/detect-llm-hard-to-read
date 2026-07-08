import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go

# ==========================================
# ⚙️ 設定エリア
# ==========================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# 各種ディレクトリへの絶対パスを構築
CSV_DIR = PROJECT_ROOT / "results" / "extracted_groups"
DATA_ROOT = PROJECT_ROOT / "data"
PARQUET_ROOT = PROJECT_ROOT / "out"  # エントロピーデータ格納用ディレクトリ

st.set_page_config(page_title="LM-CC 定性分析ビューア", layout="wide")


# ==========================================
# データの読み込み関数
# ==========================================
@st.cache_data
def load_data():
    csv_files = list(CSV_DIR.glob("extracted_groups_*.csv"))
    if not csv_files:
        return pd.DataFrame()

    df_list = [pd.read_csv(f) for f in csv_files]
    df_all = pd.concat(df_list, ignore_index=True)
    df_all = df_all.drop_duplicates(subset=['uid', 'dataset'])
    return df_all


def get_code_content(dataset, uid):
    file_path = None
    if dataset == "humaneval":
        uid_str = str(uid).replace("HumanEval_", "")
        file_path = DATA_ROOT / "humaneval" / f"HumanEval_{uid_str}.py"
    elif dataset == "xcodeeval_apr":
        file_path = DATA_ROOT / "xcodeeval" / "apr" / f"{uid}.py"
    elif dataset == "xcodeeval_code_translation":
        file_path = DATA_ROOT / "xcodeeval" / "code_translation" / f"{uid}.py"

    if file_path and file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    return f"ファイルが見つかりません: {file_path}"


def get_parquet_data(dataset, uid):
    p_path = None
    if dataset == "humaneval":
        uid_str = str(uid).replace("HumanEval_", "")
        p_path = PARQUET_ROOT / "humaneval" / f"result_HumanEval_{uid_str}.parquet"
    elif dataset == "xcodeeval_apr":
        p_path = PARQUET_ROOT / "xcodeeval_apr" / f"result_{uid}.parquet"
    elif dataset == "xcodeeval_code_translation":
        p_path = PARQUET_ROOT / "xcodeeval_code_translation" / f"result_{uid}.parquet"

    if p_path and p_path.exists():
        return pd.read_parquet(p_path)
    return None


# ==========================================
# ハイライトHTML生成関数
# ==========================================
def build_highlighted_html(raw_code, df_parquet, threshold):
    if df_parquet is None or df_parquet.empty or 'token_str' not in df_parquet.columns:
        return f"<pre><code>{raw_code}</code></pre>"

    html = '<pre style="background-color: #1e1e1e; color: #d4d4d4; padding: 15px; border-radius: 8px; line-height: 1.5; font-family: monospace; overflow-x: auto;"><code>'
    cursor = 0
    clean_code = raw_code

    for row in df_parquet.itertuples():
        if pd.isna(row.token_str): continue

        tok_str = str(row.token_str)
        tok_str = tok_str.replace(' ', ' ').replace('<0x0A>', '\n').replace('<s>', '').replace('</s>', '')
        search_str = tok_str.strip()

        if not search_str:
            continue

        idx = clean_code.find(search_str, cursor)
        if idx == -1:
            continue

        prefix = clean_code[cursor:idx]
        html += prefix.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

        matched_text = clean_code[idx:idx + len(search_str)]
        matched_esc = matched_text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

        ent = float(row.metric_entropy) if pd.notna(row.metric_entropy) else 0.0

        if ent >= threshold:
            html += f'<span style="background-color: rgba(255, 60, 60, 0.5); font-weight: bold; border-radius: 3px;" title="エントロピー: {ent:.4f}">{matched_esc}</span>'
        else:
            html += f'<span>{matched_esc}</span>'

        cursor = idx + len(search_str)

    html += clean_code[cursor:].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    html += '</code></pre>'
    return html


# ==========================================
# メインUI
# ==========================================
def main():
    st.title("🔍 LM-CC 定性分析ダッシュボード")

    df = load_data()
    if df.empty:
        st.error(f"CSVファイルが見つかりません。以下のパスにデータが出力されているか確認してください:\n`{CSV_DIR}`")
        return

    # --- サイドバー ---
    st.sidebar.header("🎯 フィルター設定")
    selected_groups = st.sidebar.multiselect(
        "グループを選択", options=["A", "B", "C"], default=["A"]
    )
    available_datasets = df['dataset'].unique().tolist()
    selected_datasets = st.sidebar.multiselect(
        "データセットを選択", options=available_datasets, default=available_datasets
    )

    filtered_df = df[
        (df['group'].isin(selected_groups)) &
        (df['dataset'].isin(selected_datasets))
        ].reset_index(drop=True)

    st.sidebar.markdown("---")
    st.sidebar.metric(label="対象コード件数", value=f"{len(filtered_df)} 件")

    if len(filtered_df) == 0:
        st.warning("条件に一致するデータがありません。")
        return

    # ==========================================
    # 🎨 レイアウトコンテナの準備（画面表示順を固定）
    # ==========================================
    info_container = st.container()  # 上部：メタ情報（UIDやLM-CCスコア）
    graph_container = st.container()  # 中部：エントロピー推移グラフ
    code_container = st.container()  # 中部：コードビューア
    st.markdown("---")  # 区切り線
    nav_container = st.container()  # 下部：操作スライダー群

    # ==========================================
    # ⚙️ ロジック実行（コンテナへの割り当て）
    # ==========================================

    # 1. ナビゲーション操作（見た目は一番下ですが、データ取得のために先に評価します）
    with nav_container:
        st.markdown("### ⚙️ コントロールパネル")
        st.markdown("**⌨️ キーボード操作:** 下のスライダーをクリックし、**左右の矢印キー（← / →）**でコードを切り替え")
        current_idx = st.slider("コードを切り替える", min_value=1, max_value=len(filtered_df), value=1) - 1

    row = filtered_df.iloc[current_idx]

    # 2. メタ情報の表示
    with info_container:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Group", row['group'])
        col2.metric("Dataset", row['dataset'])
        col3.metric("LM-CC Score", f"{row['lm_cc']:.3f}")
        col4.metric("LOC (行数)", row['loc'])
        st.markdown(f"**UID:** `{row['uid']}`")

    raw_code = get_code_content(row['dataset'], row['uid'])
    df_parquet = get_parquet_data(row['dataset'], row['uid'])

    if df_parquet is not None and not df_parquet.empty and 'metric_entropy' in df_parquet.columns:
        entropies = df_parquet['metric_entropy'].dropna().tolist()
        max_ent = max(entropies) if entropies else 1.0

        # 3. 閾値設定スライダーを下部のナビゲーションコンテナに追加
        with nav_container:
            # セッションステートの初期化（初回のみ実行）
            if 'threshold_pct' not in st.session_state:
                st.session_state.threshold_pct = 50.0

            # スライダーは「割合（％）」を選択させる
            # 💡 keyを指定することで、st.session_state['threshold_pct'] と自動連動し値が保持されます
            selected_pct = st.slider(
                "🎨 ハイライト閾値 (最大エントロピーに対する割合 %)",
                min_value=0.0, max_value=100.0, step=1.0,
                key='threshold_pct'
            )

            # 選択された割合から、実際の絶対値としての閾値を計算して適用
            threshold = float(max_ent * (selected_pct / 100.0))

            # ユーザーが現在の絶対値を確認できるように小さく表示
            st.caption(
                f"現在のハイライト基準値: **{threshold:.4f}** (最大エントロピー {max_ent:.4f} の {selected_pct}%)")

        # 4. グラフの表示
        with graph_container:
            st.markdown("---")
            st.subheader("📊 エントロピー推移")
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                y=entropies, mode='lines', name='Entropy',
                line=dict(color='rgba(255, 60, 60, 0.8)', width=1.5)
            ))
            fig.add_hline(y=threshold, line_dash="dash", line_color="yellow", annotation_text="ハイライト閾値")
            fig.update_layout(height=250, margin=dict(l=0, r=0, t=10, b=0), template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)

        # 5. コードビューアの表示
        with code_container:
            st.subheader("💻 コードビューア（マウスホバーでエントロピー数値を表示）")
            html_content = build_highlighted_html(raw_code, df_parquet, threshold)
            st.components.v1.html(html_content, height=600, scrolling=True)

    else:
        with code_container:
            st.warning("⚠️ 対応するParquetデータ（エントロピー）が見つからないため、通常のコードを表示します。")
            st.code(raw_code, language="python")


if __name__ == "__main__":
    main()