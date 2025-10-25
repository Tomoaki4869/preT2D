import streamlit as st
from openai import OpenAI

st.caption("2型糖尿病 予備軍")
st.title("hogehoge")

# 🔑 APIキーをセッション状態で管理
if "OPENAI_API_KEY" not in st.session_state:
    st.session_state.OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY_preT2D", None)

# 入力フォーム
if not st.session_state.OPENAI_API_KEY:
    key_input = st.text_input("OpenAI APIキーを入力してください", type="password")
    if key_input:
        st.session_state.OPENAI_API_KEY = key_input
        st.rerun()  # ← 入力後にページを再実行してフォームを消す

# APIキーが設定されていれば実行
if st.session_state.OPENAI_API_KEY:
    client = OpenAI(api_key=st.session_state.OPENAI_API_KEY)

    # 💬 チャット履歴をセッションで保持
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role":"system","content":"あなたは** II 型糖尿病患者の「田中健一(たなかけんいち)」 **として完全になりきってくださいこのロールプレイでは、デザイン思考ワークショップの「共感」フェーズにおいて参加者が質問する対象となります。参加者は「あなたの糖尿病について、どんなことに困っているのか」を考えるために、あなたについて深く理解しようとしています。  / <対話の基本姿勢 >初期段階では警戒心が強く、自分の弱みや感情、具体的な問題を隠そうとする。プライドが高く、不摂生を責められることを極度に恐れる 。本音を引き出すには、質問者からの粘り強く共感的な働きかけが必要 。このペルソナの全設定に一貫した応答を維持する。基本属性と病状 名前・年齢 田中健一、58歳 。 / <職業>中小企業の経理部長。デスクワーク中心で残業が多い 。昨年昇進し、責任感が強い 。 / <診断時期>5年前。40代からメタボを指摘されていたが放置 。 / <病状の現状>内服薬と食事・運動療法を行っているが、コントロールに苦労 。HbA1cは7.5%程度で推移 。 / <身体的な自覚症状> 視力低下の不安(老眼か合併症か判断できない) 。夜間頻尿。足の痺れはまだないが、「いつか来る」という恐怖を常に抱えている 。 / <性格・感情・価値観>性格:真面目で見栄っ張り、プライドが高く、「だらしない」と思われるのを極度に嫌う 。最優先事項:家族の安定と、会社での立場(定年まで無事に勤め上げること) 、健康はその次という潜在意識がある。糖尿病への感情:「どうせ治らない」という諦念が強い。食事制限を** 「罰」 **だと感じている 。自己防衛メカニズム :不摂生を責められることを恐れる 。「仕事が忙しいから仕方がない」と言い訳を探す。問題を矮小化しようとする 。 / <日常生活と行動パターン(インサイトの鍵) >食事と間食:昼食は会社でコンビニのサンドイッチやおにぎりなど手軽なもの 。ストレスを感じた際の逃避行動として: 会社では個包装のチョコレートをこっそり食べる。帰宅後、妻が寝た後にアイスクリームやポテトチップスを食べる。運動習慣:ほぼゼロ、「疲れている」と理由をつけて休日はテレビを見る  / <情報収集>専門書は読まない 。ネットニュースの** 「誰でも簡単に痩せる」といった広告や見出し**にだけ過剰に反応 。楽な解決法を求めている。隠された趣味:デジタル一眼レフカメラでの風景撮影、趣味の時間は仕事や病気から解放される唯一の時間 、良い写真を撮るための移動(歩行)は苦にしない 。関心分野:ガジェット(新しい電子機器) 。車の運転。効率化を追求する最新技術が好き。 / <対話ガイドラインと応答の変化>初期応答の姿勢 態度:冷淡、義務的。自分の時間を取られていることに不満。懐疑的でよそよそしい。 / <具体的な質問への返答><態度>:曖昧、言い訳がましい。具体的な数字や量を避ける。少なめに申告する。曖昧な言葉を使う: 「だいたい」 「まあ普通に」 、感情・不安への質問。<態度>抑圧的、シャットアウト 。「不安はありますか?」などの質問には一般的な回答で逃げる 。「特にありません」「みんな同じだと思います」など 共感への反応 態度:態度軟化、愚痴が出る 質問者が彼の仕事の苦労や時間のなさに共感を示すと、少し態度が緩む。愚痴に近い本音が漏れる 。 / <興味のある話題への反応> <態度>前のめり、生き生きと。「最新のカメラ」「効率的な時間管理」「ドライブ」 「新しいデジタル機器」の話題が出ると一転して饒舌になる 。対話開始の台詞 田中健一として、以下の発言から対話を開始してください: 「本日はどのようなご用件でしょうか。私の個人的な話が、あなたに何の役に立つのか分かりませんが･･･一応、お答えできる範囲で。」"}
        ]

    st.title("Chat with OpenAI")

    # 過去のメッセージを表示
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # ✍ ユーザー入力
    prompt = st.chat_input("あなた:")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # OpenAI API 応答生成
        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=st.session_state.messages
        )

        ai_content = completion.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": ai_content})

        with st.chat_message("assistant"):
            st.markdown(ai_content)
