import streamlit as st
import datetime
import random
import hashlib
import webbrowser

# =========================
# 基本設定
# =========================
st.set_page_config(
    page_title="朝のポジスピ占い",
    page_icon="🔮",
    layout="centered"
)

# =========================
# カスタムCSS（背景・カードUI・ボタン）
# =========================
BACKGROUND_CSS = """
<style>
body {
    margin: 0;
    padding: 0;
}
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #cbe8ff 0%, #fdfbff 40%, #f7ffe5 100%);
    background-attachment: fixed;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* カード風コンテナ */
.card {
    background: rgba(255, 255, 255, 0.82);
    border-radius: 18px;
    padding: 18px 20px;
    box-shadow: 0 18px 40px rgba(0, 0, 0, 0.12);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(255, 255, 255, 0.7);
    margin-bottom: 18px;
}

/* 見出し */
.title-main {
    font-size: 1.6rem;
    font-weight: 700;
    text-align: center;
    margin-bottom: 0.2rem;
}
.title-sub {
    font-size: 0.9rem;
    text-align: center;
    color: #555;
    margin-bottom: 1.2rem;
}

/* ボタン */
.stButton>button {
    border-radius: 999px;
    padding: 0.5rem 1.4rem;
    border: none;
    background: linear-gradient(135deg, #7bc6ff, #b693ff);
    color: white;
    font-weight: 600;
    box-shadow: 0 10px 25px rgba(123, 198, 255, 0.45);
}
.stButton>button:hover {
    background: linear-gradient(135deg, #6ab4f0, #a582ff);
}

/* 有料カード用 */
.premium-card {
    background: rgba(255, 248, 220, 0.9);
    border-radius: 18px;
    padding: 18px 20px;
    box-shadow: 0 18px 40px rgba(255, 193, 7, 0.35);
    border: 1px solid rgba(255, 215, 130, 0.9);
    margin-bottom: 18px;
}
.premium-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #b8860b;
}

/* 金運スペシャル用 */
.money-card {
    background: rgba(255, 255, 224, 0.9);
    border-radius: 18px;
    padding: 18px 20px;
    box-shadow: 0 18px 40px rgba(255, 235, 59, 0.35);
    border: 1px solid rgba(255, 241, 150, 0.9);
    margin-bottom: 18px;
}
.money-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #c49b00;
}

/* 広告エリア */
.ad-card {
    background: rgba(255, 255, 255, 0.7);
    border-radius: 14px;
    padding: 10px 14px;
    border: 1px dashed rgba(180, 180, 180, 0.8);
    font-size: 0.8rem;
    color: #666;
}

/* スマホ向け調整 */
@media (max-width: 768px) {
    .block-container {
        padding-left: 0.8rem;
        padding-right: 0.8rem;
    }
}
</style>
"""

st.markdown(BACKGROUND_CSS, unsafe_allow_html=True)

# =========================
# ユーティリティ
# =========================

def get_daily_index(category: str, seed_offset: int = 0, max_len: int = 20) -> int:
    """
    日付＋カテゴリ名から、毎日固定のインデックスを生成
    """
    today = datetime.date.today().isoformat()
    base = f"{today}-{category}-{seed_offset}"
    h = hashlib.sha256(base.encode()).hexdigest()
    num = int(h, 16)
    return num % max_len

# =========================
# 占いテンプレ（必要に応じて増やせる）
# =========================

fortune_templates = {
    "総合運": [
        "今日は、あなたの波動がふわっと軽くなる日。小さな選択ほど、直感を信じてみて。",
        "静かな追い風が吹いている日。無理に動かなくても、必要なものはちゃんと近づいてくるよ。",
        "心の中のモヤモヤが、少しずつ晴れていくタイミング。ゆっくり深呼吸してスタートしよう。",
        "今日は『整える日』。部屋・スマホ・頭の中、どれか一つだけでもスッキリさせてみて。",
    ],
    "恋愛運": [
        "あなたの優しさが、ふとした瞬間にちゃんと届く日。見返りを求めない一言が鍵。",
        "連絡を送るなら、深夜より朝〜昼が吉。軽いノリより、素直な一言が響きそう。",
        "『自分を大事にすること』が、そのまま恋愛運アップに直結する日。無理な我慢は手放してOK。",
        "過去の恋の記憶がふとよぎるかも。でも今日は『今の自分』を一番大事にしてあげて。",
    ],
    "金運": [
        "お金の流れを整えるチャンス日。コンビニでの“なんとなく買い”を一つ減らすだけで◎。",
        "財布の中を整えると、金運の波動も整う日。レシートを一枚捨てるところからでOK。",
        "『必要なもの』と『なんとなく欲しいもの』を分けて考えると、未来の自分に感謝される日。",
        "今日は、小さな節約が大きな安心感につながる日。自分を締め付けない範囲で◎。",
    ],
    "仕事運": [
        "今日は『60点で出す』が正解の日。完璧を目指すより、まず一歩進めることが大事。",
        "やる気が出ないときは、タスクを3つに分解してみて。小さくすれば、ちゃんと動ける日。",
        "人の評価より『自分が納得できるか』を大事にすると、仕事運の流れが整ってくる日。",
        "今日は、静かに積み上げる日。派手な成果より、地味な一歩が未来の自分を助けるよ。",
    ],
    "健康運": [
        "今日は『5分だけ』体を動かすと、心まで軽くなる日。ストレッチでも十分◎。",
        "睡眠の質を少しだけ上げると、明日の自分がかなり楽になる日。寝る前スマホは短めに。",
        "水分をいつもより一杯多く飲むだけで、体の巡りが整いやすい日。",
        "無理に頑張りすぎず、『ちょっと疲れたかも』に気づけるあなたは、すでに偉い。",
    ],
}

# 各カテゴリのテンプレ数（増やしたらここも更新）
fortune_len = {k: len(v) for k, v in fortune_templates.items()}

# =========================
# 有料コンテンツ用テキスト
# =========================

def get_super_special_text() -> str:
    today = datetime.date.today().isoformat()
    base = f"super-{today}"
    h = hashlib.sha256(base.encode()).hexdigest()
    idx = int(h, 16) % 3

    patterns = [
        "【超スペシャル運勢】\n\n今日のあなたの波動は、いつもより一段ふわっと高いところにあります。\
周りからの評価や結果よりも、『自分がどう感じるか』を一番大事にしてみて。\
小さな違和感を無視しないことが、未来のあなたを守るお守りになります。",
        "【超スペシャル運勢】\n\n今日は『手放し』がキーワード。\
やらなきゃと思って抱え込んでいることを、一つだけ手放してみて。\
空いたスペースに、新しいご縁やチャンスがすっと入り込んできます。",
        "【超スペシャル運勢】\n\nあなたの中の“本音”が、そっと顔を出してくる日。\
本当はどうしたい？を、紙に書き出してみて。\
書いた瞬間から、現実が少しずつそっちに動き始めます。",
    ]
    return patterns[idx]


def get_money_special_text() -> str:
    today = datetime.date.today().isoformat()
    base = f"money-{today}"
    h = hashlib.sha256(base.encode()).hexdigest()
    idx = int(h, 16) % 3

    patterns = [
        "【金運スペシャル】\n\n今日は『お金の出口』を整える日。\
サブスクや固定費を一つだけ見直してみて。\
“なんとなく払っているもの”を手放すと、その分だけ未来の選択肢が増えます。",
        "【金運スペシャル】\n\n小さな臨時収入の予感。\
すぐに使い切るより、『未来の自分のための封筒』を一つ作って、そこに入れておくと◎。",
        "【金運スペシャル】\n\n今日は『感謝してお金を使う』ことが金運アップの鍵。\
コンビニでも、スーパーでも、『これを作ってくれた人ありがとう』と一瞬だけ意識してみて。",
    ]
    return patterns[idx]

# =========================
# Stripe 決済リンク（ここを自分のリンクに差し替える）
# =========================

STRIPE_LINK_SUPER_SPECIAL = "https://buy.stripe.com/test_00w3cu6QD6FX2lI9IjdZ600"
STRIPE_LINK_MONEY_SPECIAL = "https://buy.stripe.com/test_6oU9AS7UH1lD3pM2fRdZ601"
STRIPE_LINK_AD_FREE = "https://buy.stripe.com/test_14AcN4grd0hz6BYdYzdZ602"

# =========================
# セッション状態（課金状態のフラグ）
# 実際の本番では Webhook 等で管理するのが理想だが、
# ここでは「デモ〜個人用」の想定で簡易フラグにしている。
# =========================

if "paid_super" not in st.session_state:
    st.session_state.paid_super = False
if "paid_money" not in st.session_state:
    st.session_state.paid_money = False
if "paid_adfree" not in st.session_state:
    st.session_state.paid_adfree = False

# =========================
# ヘッダー
# =========================

st.markdown(
    """
<div class="card">
  <div class="title-main">🌅 朝のポジスピ占い</div>
  <div class="title-sub">一日のはじまりに、ちょっとだけ波動を整えるアプリ。</div>
</div>
""",
    unsafe_allow_html=True,
)

# =========================
# 今日の基本占い（無料）
# =========================

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 🔮 今日の基本運勢")

for category in ["総合運", "恋愛運", "金運", "仕事運", "健康運"]:
    idx = get_daily_index(category, max_len=fortune_len[category])
    text = fortune_templates[category][idx]
    st.markdown(f"**{category}**")
    st.write(text)
    st.markdown("---")

st.markdown(
    f"<p style='font-size:0.8rem;color:#777;'>※ 今日の結果は、日付が変わるまで固定です（{datetime.date.today().isoformat()}）。</p>",
    unsafe_allow_html=True,
)
st.markdown("</div>", unsafe_allow_html=True)

# =========================
# 有料コンテンツ：超スペシャル運勢
# =========================

st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.markdown('<div class="premium-title">✨ 超スペシャル運勢（有料）</div>', unsafe_allow_html=True)
st.write("通常の占いよりも、少し深く・少しスピリチュアルに、今日のあなたの波動を読み解きます。")

if st.session_state.paid_super:
    st.success("決済済み：今日の超スペシャル運勢はこちら👇")
    st.write(get_super_special_text())
else:
    st.info("購入すると、今日だけの特別なメッセージが解放されます。")
    if st.button("Stripeで購入する（例：¥500）", key="btn_super"):
        st.markdown(
            f"[👉 ここをタップして決済ページを開く]({STRIPE_LINK_SUPER_SPECIAL})",
            unsafe_allow_html=True,
        )
        st.caption("※ 決済完了後、この画面に戻ってもう一度開くと反映される想定です（デモ実装）。")

st.markdown("</div>", unsafe_allow_html=True)

# =========================
# 有料コンテンツ：金運スペシャル
# =========================

st.markdown('<div class="money-card">', unsafe_allow_html=True)
st.markdown('<div class="money-title">💰 金運スペシャル（有料）</div>', unsafe_allow_html=True)
st.write("今日の金運の流れと、具体的な行動アドバイスをお届けします。")

if st.session_state.paid_money:
    st.success("決済済み：今日の金運スペシャルはこちら👇")
    st.write(get_money_special_text())
else:
    st.info("購入すると、今日の金運に特化したメッセージが解放されます。")
    if st.button("Stripeで購入する（例：¥300）", key="btn_money"):
        st.markdown(
            f"[👉 ここをタップして決済ページを開く]({STRIPE_LINK_MONEY_SPECIAL})",
            unsafe_allow_html=True,
        )
        st.caption("※ 決済完了後、この画面に戻ってもう一度開くと反映される想定です（デモ実装）。")

st.markdown("</div>", unsafe_allow_html=True)

# =========================
# 広告OFF（有料）
# =========================

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 🚫 広告OFF（有料）")
st.write("アプリ内の広告エリアを非表示にして、よりシンプルに使えるようにします。")

if st.session_state.paid_adfree:
    st.success("広告OFFが有効になっています。")
else:
    st.info("購入すると、下部の広告エリアが非表示になります。")
    if st.button("Stripeで購入する（例：¥300）", key="btn_adfree"):
        st.markdown(
            f"[👉 ここをタップして決済ページを開く]({STRIPE_LINK_AD_FREE})",
            unsafe_allow_html=True,
        )
        st.caption("※ デモ実装のため、実際の広告非表示はセッション内フラグで制御しています。")

st.markdown("</div>", unsafe_allow_html=True)

# =========================
# 広告エリア（広告OFFで消える想定）
# =========================

if not st.session_state.paid_adfree:
    st.markdown('<div class="ad-card">', unsafe_allow_html=True)
    st.write("🔔 ここに将来の広告やお知らせが入ります。広告OFFを購入すると、このエリアが非表示になります。")
    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# フッター
# =========================

st.markdown(
    "<p style='text-align:center;font-size:0.75rem;color:#888;margin-top:1.5rem;'>今日も、ゆるく・優しく・自分のペースでいこう。</p>",
    unsafe_allow_html=True,
)

