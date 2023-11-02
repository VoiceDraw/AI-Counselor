
import streamlit as st
import openai
from langdetect import detect  # langdetectパッケージをインポート

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets["OpenAIAPI"]["openai_api_key"]

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "あなたは優秀なアシスタントAIです。"}
    ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_input = st.session_state["user_input"]

    # 入力の言語を検出
    detected_language = detect(user_input)

    # 日本語以外の言語の入力を無視
    if detected_language != 'ja':
        st.warning("日本語以外の言語はサポートされていません。")
        return

    user_message = {"role": "user", "content": user_input}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    
    # AIの応答が読解不能な場合を処理
    if "この要求はタイムアウトしました" in bot_message:  # タイムアウトエラーメッセージを検出
        st.warning("AIの応答が読解不能でした。もう一度試してください。")
    else:
        messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去

# ユーザーインターフェイスの構築
st.title("My AI Assistant")
st.write("ChatGPT APIを使ったチャットボットです。")

user_input = st.text_input("メッセージを入力してください。", key="user_input")

if st.button("送信"):  # 送信ボタンがクリックされたときに動作
    communicate()

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"] == "assistant":
            speaker = "🤖"

        st.write(speaker + ": " + message["content"])

