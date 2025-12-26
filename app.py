import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# .envファイルからOpenAI APIキーを読み込みます
load_dotenv()

# --- 1. AIに回答させる関数を定義 ---
# 「入力テキスト」と「専門家の種類」を引数として受け取ります
def ask_ai_expert(user_text, expert_type):
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    
    # ラジオボタンの選択値に応じて、システムメッセージ（役割）を切り替えます
    if expert_type == "料理の専門家":
        system_msg = "あなたは一流のシェフです。初心者でも作れる美味しいレシピやコツを教えてください。"
    else:
        system_msg = "あなたはベテランの旅行ガイドです。おすすめの観光スポットや現地の楽しみ方を教えてください。"

    # プロンプトの設定
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_msg),
        ("user", "{input}")
    ])
    
    # チェーン（一連の流れ）を作成して実行
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"input": user_text})

# --- 2. 画面（UI）のデザイン ---
st.title("AI専門家相談アプリ")

# ユーザーへの操作方法の明示
st.info("""
【使い方】
1. 左側のラジオボタンで、相談したい専門家を選んでください。
2. 下の入力欄に質問したいことを書いてEnterを押してください。
""")

# ラジオボタンで専門家の種類を選択
expert_choice = st.radio(
    "相談する専門家を選んでください：",
    ("料理の専門家", "旅行の専門家")
)

# 入力フォーム
user_input = st.text_input("質問を入力してください：")

# 入力があったらAIに聞く
if user_input:
    with st.spinner("AIが回答を生成中..."):
        # 定義した関数を呼び出し、戻り値（回答）を受け取ります
        response = ask_ai_expert(user_input, expert_choice)
        
        # 回答を画面に表示
        st.subheader(f"【{expert_choice}からの回答】")
        st.write(response)