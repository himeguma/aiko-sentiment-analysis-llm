import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import ast
from sklearn.metrics.pairwise import cosine_similarity


def dataframe_row_selection_change() -> None:
    """データフレームの行選択の変更時に動作"""
    try:
        print(st.session_state.data.selection["rows"])
    except:
        pass


# 各行で変換を行う関数
def convert_image_urls(row):
    """写真のURLの表示を適正化する関数

    :param row: 該当列の文字列
    :type row: str
    :return: URL
    :rtype: str
    """
    return ast.literal_eval(ast.literal_eval(row)[0])[0]


def plot_radar_chart_graph(values):
    """各感情の値に応じたレーダーグラフを作成する

    :param values: 感情のスコア
    :type values: int
    :return: レーダーグラフ
    :rtype: fig
    """
    # 感情軸とスコアの設定（画像と同じ順序で）
    categories = [
        "恐れ",
        "信頼",
        "喜び",
        "期待",
        "怒り",
        "嫌悪",
        "悲しみ",
        "驚き",
    ]

    # 各感情に対応する色設定（画像に合わせた色）
    COLORS = {
        "恐れ": "#355E3B",
        "信頼": "#6B8E23",
        "喜び": "#FFD966",
        "期待": "#FFB347",
        "怒り": "#D9534F",
        "嫌悪": "#7D3C98",
        "悲しみ": "#2F4F6F",
        "驚き": "#5DADE2",
    }

    # 各軸に表示するテキスト（感情名とスコアを組み合わせる）
    category_labels = [
        f"{category}: {value}" for category, value in zip(categories, values)
    ]

    # レーダーチャートの生成
    fig = go.Figure()

    # 各感情軸にスコアをプロット（軸と線は黒）
    fig.add_trace(
        go.Scatterpolar(
            r=values + [values[0]],  # 最後の値を最初に戻すことで閉じる
            theta=category_labels
            + [category_labels[0]],  # ラベルにスコアを含める
            line=dict(color="red"),
            marker=dict(size=8),
        )
    )

    # 各感情のセクションごとに色を適用（点は各感情ごとに色分け）
    for i, category in enumerate(categories):
        fig.add_trace(
            go.Scatterpolar(
                r=[values[i]],  # 各感情のスコアを設定
                theta=[category_labels[i]],
                mode="markers",
                marker=dict(color=COLORS[category], size=12),
                showlegend=False,
            )
        )
    # インタラクションを完全に無効化
    fig.update_layout(dragmode=False)
    # レーダーチャートのレイアウト設定（軸と目盛りは黒）
    fig.update_layout(
        width=500,  # 横幅を設定
        height=500,  # 高さを設定
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],  # スコア範囲を0-100に設定
                tickfont=dict(size=14, color="black"),
                linecolor="black",
            ),
            angularaxis=dict(
                tickfont=dict(size=14, color="black"),
                linecolor="black",
            ),
        ),
        margin=dict(l=60, r=60, t=60, b=60),
        showlegend=False,
    )

    return fig


@st.cache_data(show_spinner=False)
def load_df():
    """dfの読み込みを高速化する

    :return: 加工済みdf
    :rtype: Dataframe
    """
    # CSV読み込み
    df = pd.read_csv(
        r"aikohomepage_track_lyrics_emotion.csv",
        encoding="utf-8-sig",
        index_col=0,
    )
    # 体裁調整
    df["曲名"] = df["track_name"]
    # 画像に変換
    df["converted_image_urls"] = df["image_urls"].apply(convert_image_urls)

    return df


@st.dialog("8つの感情とは", width="large")
def emotion_discription():
    st.write(r"人間には8つの感情があります")
    st.write(r"（心理学者のプルチックが考えました）")
    for each_emotion, each_emotion_discription in zip(
        EMOTION_LIST, EMOTION_DISCRIPTION_LIST
    ):
        # 感情ごとに色を変えて得点とその理由を表示
        st.write(
            f"<span style='background-color: {COLORS[each_emotion]}; padding: 4px; border-radius: 4px;'>　　</span> {each_emotion}…{each_emotion_discription}",
            unsafe_allow_html=True,
        )
    if st.button("閉じる"):
        st.rerun()


# 感情名のリスト
EMOTION_LIST = [
    "喜び",
    "信頼",
    "恐れ",
    "驚き",
    "悲しみ",
    "嫌悪",
    "怒り",
    "期待",
]
# グラフ表示用感情名のリスト
EMOTION_GRAPH = [
    "恐れ",
    "信頼",
    "喜び",
    "期待",
    "怒り",
    "嫌悪",
    "悲しみ",
    "驚き",
]
# 色の辞書
COLORS = {
    "恐れ": "#355E3B",
    "信頼": "#6B8E23",
    "喜び": "#FFD966",
    "期待": "#FFB347",
    "怒り": "#D9534F",
    "嫌悪": "#7D3C98",
    "悲しみ": "#2F4F6F",
    "驚き": "#5DADE2",
}
EMOTION_DISCRIPTION_LIST = [
    "希望が達成された時や、優しさを感じたときのさわやかな気持ち",
    "心配することなく、信じて安心できる気持ち",
    "害悪や危険な事柄に対して逃避したいと感じる気持ち",
    "予期しない事象を体験したときの瞬間的な気持ち",
    "物事がうまくいかなかったときや、大切なものを失ったときに感じる残念な気持ち",
    "憎み嫌い、不快に感じる気持ち",
    "侮辱されたり傷つけられたりしたときに起こる不愉快な気持ち",
    "事柄が自分の思い通りになることを望む気持ち",
]
df = load_df()

# =================================================================================
# config
st.set_page_config(
    page_title="aikoの歌詞_感情分析ツール",
    page_icon=":musical_note:",
    layout="wide",
    menu_items={"About": "app created by himeguma"},
)
# 表示
st.header(
    ":musical_note: あなたの好きなaikoの曲を分析します！",
    anchor=False,
    divider="rainbow",
)

st.write("")

options = st.multiselect(
    "好きな曲を選んでください（複数選べます）",
    df["track_name"],
    placeholder="全曲リスト（リリース時期順）",
    label_visibility="visible",
)

if options:
    # マルチセレクトのアクティブ時
    # 選択した曲に絞り込み
    selected_df = df[df["track_name"].isin(options)]
    # 表示するものに絞り込む
    selected_df_display = selected_df[
        ["曲名", "converted_image_urls"] + EMOTION_LIST
    ]

    st.write("")
    if st.button("8つの感情とは？　▼"):
        emotion_discription()

    st.write("↓　歌詞の感情を100点満点で点数をつけました")
    # 選択した曲の表示
    st.dataframe(
        selected_df_display,
        column_config={
            "converted_image_urls": st.column_config.ImageColumn(
                "写真", width=None
            ),
            "喜び": st.column_config.ProgressColumn(
                "喜び", format="%f", min_value=0, max_value=100, width="small"
            ),
            "信頼": st.column_config.ProgressColumn(
                "信頼", format="%f", min_value=0, max_value=100, width="small"
            ),
            "恐れ": st.column_config.ProgressColumn(
                "恐れ", format="%f", min_value=0, max_value=100, width="small"
            ),
            "驚き": st.column_config.ProgressColumn(
                "驚き", format="%f", min_value=0, max_value=100, width="small"
            ),
            "悲しみ": st.column_config.ProgressColumn(
                "悲しみ",
                format="%f",
                min_value=0,
                max_value=100,
                width="small",
            ),
            "嫌悪": st.column_config.ProgressColumn(
                "嫌悪", format="%f", min_value=0, max_value=100, width="small"
            ),
            "怒り": st.column_config.ProgressColumn(
                "怒り", format="%f", min_value=0, max_value=100, width="small"
            ),
            "期待": st.column_config.ProgressColumn(
                "期待", format="%f", min_value=0, max_value=100, width="small"
            ),
        },
        use_container_width=False,
        hide_index=True,
    )

    st.write("")

    # expanderで理由書きの表示
    with st.expander("点数の理由はここをクリック　▼"):

        st.write("")

        if len(options) > 1:
            st.write("※下の曲名を押すと曲を切り替えられます")
        # 選ばれた曲ごとにタブを動的に生成
        tab_objects = st.tabs(options)

        # 各タブに対応するコンテンツを表示
        for tab, each_option in zip(tab_objects, options):
            with tab:
                for each_emotion in EMOTION_LIST:
                    # 感情ごとに色を変えて得点とその理由を表示
                    st.write(
                        f"<span style='background-color: {COLORS[each_emotion]}; padding: 4px; border-radius: 4px;'>　　</span> {each_emotion}　{str(
                                    selected_df[selected_df["曲名"] == each_option][
                                        each_emotion
                                    ].values[0]
                                )}点 <span style='background-color: {COLORS[each_emotion]}; padding: 4px; border-radius: 4px;'>　　</span>",
                        unsafe_allow_html=True,
                    )
                    st.write(
                        selected_df[selected_df["曲名"] == each_option][
                            each_emotion + "スコアの理由"
                        ].values[0]
                    )

    st.write("")

    # 選択範囲のチャートを表示
    st.subheader(
        ":chart_with_upwards_trend:感情グラフ",
        anchor=False,
        divider="red",
    )
    # グラフに表示するために得点を記録
    values = selected_df[EMOTION_GRAPH].mean().astype(int).to_list()

    # 各感情とその平均スコアをタプルのリストにする
    emotion_scores = list(zip(EMOTION_GRAPH, values))

    # スコアの高い順にソート
    top_emotions = sorted(emotion_scores, key=lambda x: x[1], reverse=True)[:1]

    st.write("")

    st.write(
        f"あなたは**{top_emotions[0][0]}**が大きい曲が好きなのかもしれません"
    )
    # レーダーチャートを表示
    st.plotly_chart(
        plot_radar_chart_graph(values),
        use_container_width=True,
        config={"displayModeBar": False},
    )

    st.write("")

    # マルチセレクトのアクティブ時
    st.subheader(
        "あなたの好きな曲に似た感情の曲",
        anchor=False,
        divider="red",
    )

    # 選択されたスコアの値
    selected_song_scores = pd.DataFrame(values).T
    # コサイン類似度を計算
    df_emotion = df[EMOTION_GRAPH]
    similarities = cosine_similarity(selected_song_scores, df_emotion)[0]

    # 類似度に基づきデータフレームに新しい列を追加
    df_emotion["similarity"] = similarities

    # 類似度が高い順にソート
    top_similar_df = df_emotion.sort_values(by="similarity", ascending=False)

    # 類似度の高い曲の元の情報を参照
    df_similarity = df.loc[top_similar_df.index.to_list()]
    # 選択済みの曲は除外
    df_similarity = df_similarity[~df_similarity["曲名"].isin(options)]
    # 順位の列を追加する
    df_similarity["順位"] = range(1, len(df_similarity) + 1)
    df_similarity["順位"] = df_similarity["順位"].astype(str) + "位"

    # 表示するものに絞り込む
    df_similarity_display = df_similarity[
        ["順位", "曲名", "converted_image_urls"] + EMOTION_LIST
    ].head(n=10)

    st.write(":medal:**1位は...**")

    st.image(
        df_similarity_display[df_similarity["順位"] == "1位"][
            "converted_image_urls"
        ].values[0],
        width=500,
    )
    st.write(
        f"**{df_similarity_display[df_similarity["順位"] == "1位"]["曲名"].values[0]}**　です！"
    )
    st.write("")

    # 類似度の高い曲の表示
    st.dataframe(
        df_similarity_display,
        column_config={
            "converted_image_urls": st.column_config.ImageColumn(
                "写真", width=None
            ),
            "喜び": st.column_config.ProgressColumn(
                "喜び", format="%f", min_value=0, max_value=100, width="small"
            ),
            "信頼": st.column_config.ProgressColumn(
                "信頼", format="%f", min_value=0, max_value=100, width="small"
            ),
            "恐れ": st.column_config.ProgressColumn(
                "恐れ", format="%f", min_value=0, max_value=100, width="small"
            ),
            "驚き": st.column_config.ProgressColumn(
                "驚き", format="%f", min_value=0, max_value=100, width="small"
            ),
            "悲しみ": st.column_config.ProgressColumn(
                "悲しみ",
                format="%f",
                min_value=0,
                max_value=100,
                width="small",
            ),
            "嫌悪": st.column_config.ProgressColumn(
                "嫌悪", format="%f", min_value=0, max_value=100, width="small"
            ),
            "怒り": st.column_config.ProgressColumn(
                "怒り", format="%f", min_value=0, max_value=100, width="small"
            ),
            "期待": st.column_config.ProgressColumn(
                "期待", format="%f", min_value=0, max_value=100, width="small"
            ),
        },
        use_container_width=False,
        hide_index=True,
    )

st.write("")
st.divider()
st.write("")

st.subheader(
    "感情別曲ランキング",
    anchor=False,
    divider="red",
)
st.write("")
st.write("感情を選択すると、感情別に曲を並び替えられます")

# セレクトボックスは横並びに表示
col_select1, col_select2 = st.columns([1, 1])

with col_select1:
    # 感情を選択
    selected_emotion = st.selectbox(
        "感情を選択してください",
        EMOTION_LIST,
        index=None,
        placeholder="感情を選択してください",
        label_visibility="collapsed",
    )
with col_select2:
    if selected_emotion:
        # 昇順降順を選択
        ascending_select = st.selectbox(
            "昇順降順",
            ["の大きい順", "の小さい順"],
            label_visibility="collapsed",
        )
        # boolean型に変更
        if ascending_select == "の大きい順":
            ascending_flg = False
        else:
            ascending_flg = True

if selected_emotion:
    # 感情が選択時に表示
    # 並び替えて表示
    df_selected_emotion = df.sort_values(
        selected_emotion, ascending=ascending_flg
    ).reset_index(drop=True)
    # 順位の列を追加する
    df_selected_emotion["順位"] = range(1, len(df_selected_emotion) + 1)
    df_selected_emotion["順位"] = (
        df_selected_emotion["順位"].astype(str) + "位"
    )

    # 表示するものに絞り込む
    df_selected_emotion_display = df_selected_emotion[
        ["順位", "曲名", "converted_image_urls"] + EMOTION_LIST
    ]

    # 感情順に表示
    st.dataframe(
        df_selected_emotion_display,
        column_config={
            "converted_image_urls": st.column_config.ImageColumn(
                "写真", width=None
            ),
            "喜び": st.column_config.ProgressColumn(
                "喜び", format="%f", min_value=0, max_value=100, width="small"
            ),
            "信頼": st.column_config.ProgressColumn(
                "信頼", format="%f", min_value=0, max_value=100, width="small"
            ),
            "恐れ": st.column_config.ProgressColumn(
                "恐れ", format="%f", min_value=0, max_value=100, width="small"
            ),
            "驚き": st.column_config.ProgressColumn(
                "驚き", format="%f", min_value=0, max_value=100, width="small"
            ),
            "悲しみ": st.column_config.ProgressColumn(
                "悲しみ",
                format="%f",
                min_value=0,
                max_value=100,
                width="small",
            ),
            "嫌悪": st.column_config.ProgressColumn(
                "嫌悪", format="%f", min_value=0, max_value=100, width="small"
            ),
            "怒り": st.column_config.ProgressColumn(
                "怒り", format="%f", min_value=0, max_value=100, width="small"
            ),
            "期待": st.column_config.ProgressColumn(
                "期待", format="%f", min_value=0, max_value=100, width="small"
            ),
        },
        use_container_width=False,
        hide_index=True,
        on_select=dataframe_row_selection_change,
        selection_mode=["single-row"],
        key="data",
    )

    st.write(":arrow_up:**この列を押すと分析結果がでます**")

    # データフレームの列が選択された際のみ実行
    if "data" in st.session_state:
        if "selection" in st.session_state.data:
            if "rows" in st.session_state.data.selection:
                if st.session_state.data.selection.rows:
                    # 選択された曲の読み込み
                    selected_song = df_selected_emotion_display.iloc[
                        st.session_state.data.selection.rows
                    ]["曲名"].values[0]

                    # 枠を表示
                    with st.container(border=True):
                        st.write(
                            f":red-background[**{selected_song}**]の感情分析"
                        )
                        st.write("")

                        # 感情ごとに色を変えて得点とその理由を表示
                        for each_emotion in EMOTION_LIST:
                            st.write(
                                f"<span style='background-color: {COLORS[each_emotion]}; padding: 4px; border-radius: 4px;'>　　</span> {each_emotion}　{str(
                                            df[df["曲名"] == selected_song][
                                                each_emotion
                                            ].values[0]
                                        )}点 <span style='background-color: {COLORS[each_emotion]}; padding: 4px; border-radius: 4px;'>　　</span>",
                                unsafe_allow_html=True,
                            )
                            st.write(
                                df[df["曲名"] == selected_song][
                                    each_emotion + "スコアの理由"
                                ].values[0]
                            )
