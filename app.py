import streamlit as st
import datetime
import hashlib

# =========================
# 基本設定
# =========================
st.set_page_config(
    page_title="朝のポジスピ占い",
    page_icon="🌅",
    layout="centered"
)

# =========================
# カスタムCSS（背景・カードUI）
# =========================
BACKGROUND_CSS = """
<style>
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

/* タイトル（オレンジ） */
h2 {
    color: #FF8F00 !important;
    text-shadow: 1px 1px 3px #ffffff;
}

/* サブタイトル（オレンジ） */
.subtitle-orange {
    color: #FF8F00 !important;
    text-shadow: 1px 1px 2px #ffffff;
}

/* 5カテゴリーの見出し（h3）だけオレンジ */
h3 {
    color: #FF8F00 !important;
    font-weight: 700 !important;
}

/* 本文だけ黒にする（最重要） */
.category-text {
    color: #222 !important;
    font-size: 1rem;
}

/* 有料説明や広告説明はオレンジ */
.orange-text {
    color: #FF8F00 !important;
}

/* カード */
.card {
    background: rgba(255, 255, 255, 0.82);
    border-radius: 18px;
    padding: 18px 20px;
    box-shadow: 0 18px 40px rgba(0, 0, 0, 0.12);
    backdrop-filter: blur(14px);
    border: 1px solid rgba(255, 255, 255, 0.7);
    margin-bottom: 18px;
}

/* 有料カード */
.premium-card {
    background: rgba(255, 248, 220, 0.9);
    border-radius: 18px;
    padding: 18px 20px;
    box-shadow: 0 18px 40px rgba(255, 193, 7, 0.35);
    border: 1px solid rgba(255, 215, 130, 0.9);
    margin-bottom: 18px;
}
.money-card {
    background: rgba(255, 255, 224, 0.9);
    border-radius: 18px;
    padding: 18px 20px;
    box-shadow: 0 18px 40px rgba(255, 235, 59, 0.35);
    border: 1px solid rgba(255, 241, 150, 0.9);
    margin-bottom: 18px;
}

/* 広告 */
.ad-card {
    background: rgba(255, 255, 255, 0.7);
    border-radius: 14px;
    padding: 10px 14px;
    border: 1px dashed rgba(180, 180, 180, 0.8);
    font-size: 0.8rem;
    color: #FF8F00 !important;
}
</style>
"""
st.markdown(BACKGROUND_CSS, unsafe_allow_html=True)

# =========================
# 日替わり固定ロジック
# =========================
def get_daily_index(category: str, max_len: int = 20) -> int:
    today = datetime.date.today().isoformat()
    base = f"{today}-{category}"
    h = hashlib.sha256(base.encode()).hexdigest()
    return int(h, 16) % max_len

# =========================
# 5カテゴリーのテンプレ
# =========================

positive_list = [
    "今日はあなたの心がふわっと軽くなる日。小さな選択ほど直感でOK。",
    "静かに追い風が吹く日。無理しなくても流れが整うよ。",
    "心のモヤが少し晴れる日。深呼吸してスタートしよう。",
    "今日は“整える日”。部屋かスマホか頭の中、どれか一つだけ整えてみて。",
]

spiritual_list = [
    "今日は“気づき”がテーマ。ふとした違和感を大事にしてみて。",
    "あなたの波動が少し上がる日。優しい選択が吉。",
    "直感が冴える日。最初に浮かんだ答えが正解。",
    "心の奥の本音が静かに顔を出す日。無視しないであげて。",
]

lucky_action_list = [
    "5分だけ散歩する。",
    "飲み物を一杯ゆっくり味わう。",
    "スマホの写真を3枚だけ消す。",
    "深呼吸を3回する。",
]

funny_list = [
    "今日のあなたは“意味不明な強運モード”。とりあえず胸を張って歩こう。",
    "宇宙があなたに“まあいけるっしょ”と言っている日。",
    "今日のラッキーワードは『ぬるっと』。意味はない。",
    "あなたのオーラが“ちょいバグり気味”。いい意味で。",
]

lucky_item_list = [
    "透明な飲み物",
    "四角いもの",
    "青い何か",
    "ポケットに入るサイズの物",
]

# =========================
# Stripe 決済リンク
# =========================
STRIPE_LINK_SUPER_SPECIAL = "https://buy.stripe.com/test_00w3cu6QD6FX2lI9IjdZ600"
STRIPE_LINK_MONEY_SPECIAL = "https://buy.stripe.com/test_6oU9AS7UH1lD3pM2fRdZ601"
STRIPE_LINK_AD_FREE = "https://buy.stripe.com/test_14AcN4grd0hz6BYdYzdZ602"

# =========================
# セッションフラグ
# =========================
if "paid_super" not in st.session_state:
    st.session_state.paid_super = False
if "paid_money" not in st.session_state:
    st.session_state.paid_money = False
if "paid_adfree" not in st.session_state:
    st.session_state.paid_adfree = False

# =========================
# ヘッダー（オレンジ）
# =========================
st.markdown(
    """
<div class="card">
  <h2 style="text-align:center;">🌅 朝のポジスピ占い</h2>
  <p class="subtitle-orange" style="text-align:center;">一日のはじまりに、ちょっとだけ波動を整えるアプリ。</p>
</div>
""",
    unsafe_allow_html=True,
)

# =========================
# 5カテゴリー（無料）
# =========================
st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown("### 🔮 今日のポジティブ運勢")
st.markdown(f"<p class='category-text'>{positive_list[get_daily_index('positive', len(positive_list))]}</p>", unsafe_allow_html=True)

st.markdown("### ✨ 今日のスピリチュアルメッセージ")
st.markdown(f"<p class='category-text'>{spiritual_list[get_daily_index('spiritual', len(spiritual_list))]}</p>", unsafe_allow_html=True)

st.markdown("### 🚶 今日のラッキーアクション")
st.markdown(f"<p class='category-text'>{lucky_action_list[get_daily_index('action', len(lucky_action_list))]}</p>", unsafe_allow_html=True)

st.markdown("### 😂 今日の笑える一言（意味不明系）")
st.markdown(f"<p class='category-text'>{funny_list[get_daily_index('funny', len(funny_list))]}</p>", unsafe_allow_html=True)

st.markdown("### 🎁 今日のラッキーアイテム")
st.markdown(f"<p class='category-text'>{lucky_item_list[get_daily_index('item', len(lucky_item_list))]}</p>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# =========================
# 有料：超スペシャル運勢
# =========================
st.markdown('<div class="premium-card">', unsafe_allow_html=True)
st.markdown("<h3>✨ 超スペシャル運勢（有料）</h3>", unsafe_allow_html=True)

if st.session_state.paid_super:
    st.success("決済済み：今日の超スペシャル運勢はこちら👇")
    st.markdown("<p class='category-text'>今日のあなたの波動は、いつもより一段ふわっと高いところにあります。</p>", unsafe_allow_html=True)
else:
    st.markdown("<p class='orange-text'>購入すると、今日だけの特別なメッセージが解放されます。</p>", unsafe_allow_html=True)
    if st.button("Stripeで購入する（¥500）", key="btn_super"):
        st.markdown(f"[👉 決済ページを開く]({STRIPE_LINK_SUPER_SPECIAL})", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# =========================
# 有料：金運スペシャル
# =========================
st.markdown('<div class="money-card">', unsafe_allow_html=True)
st.markdown("<h3>💰 金運スペシャル（有料）</h3>", unsafe_allow_html=True)

if st.session_state.paid_money:
    st.success("決済済み：今日の金運スペシャルはこちら👇")
    st.markdown("<p class='category-text'>今日は『お金の出口』を整える日。サブスクを一つ見直すと吉。</p>", unsafe_allow_html=True)
else:
    st.markdown("<p class='orange-text'>購入すると、今日の金運に特化したメッセージが解放されます。</p>", unsafe_allow_html=True)
    if st.button("Stripeで購入する（¥300）", key="btn_money"):
        st.markdown(f"[👉 決済ページを開く]({STRIPE_LINK_MONEY_SPECIAL})", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# =========================
# 広告OFF
# =========================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("<h3>🚫 広告OFF（有料）</h3>", unsafe_allow_html=True)

if st.session_state.paid_adfree:
    st.success("広告OFFが有効です。")
else:
    st.markdown("<p class='orange-text'>購入すると、下部の広告エリアが非表示になります。</p>", unsafe_allow_html=True)
    if st.button("Stripeで購入する（¥300）", key="btn_adfree"):
        st.markdown(f"[👉 決済ページを開く]({STRIPE_LINK_AD_FREE})", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# =========================
# 広告エリア
# =========================
if not st.session_state.paid_adfree:
    st.markdown('<div class="ad-card">🔔 ここに広告が入ります（広告OFFで非表示）</div>', unsafe_allow_html=True)

# =========================
# フッター
# =========================
st.markdown(
    "<p style='text-align:center;font-size:0.75rem;margin-top:1.5rem;color:#FF8F00;'>今日も、ゆるく・優しく・自分のペースでいこう。</p>",
    unsafe_allow_html=True,
)
