import os
import streamlit as st
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

st.title("サンプルアプリ③: LLM専門家相談アプリ")

st.write("##### 専門家の種類を選び、質問を入力すると、その分野に応じた回答が得られます。")
st.write("医師・弁護士・ITエンジニアの3名の専門家があなたの質問に答えてくれます。")

# 選択肢の日本語表示
selected_expert = st.radio(
    "相談したい専門家を選択してください。",
    ["医師", "弁護士", "ITエンジニア"]
)

st.divider()

# 入力欄（sample_app.py風にtext_inputで単文前提）
user_input = st.text_input(label="相談内容を入力してください。")

# 実行ボタン（sample_app.pyと同様）
if st.button("実行"):
    st.divider()

    if not user_input:
        st.error("質問内容を入力してください。")
    else:
        # 専門家に応じたプロンプト設定
        expert_prompt_map = {
            "医師": "あなたは非常に有能で信頼できる医師です。健康に関する相談に的確かつ優しく答えます。",
            "弁護士": "あなたは経験豊富な弁護士です。法律に関する質問に明快なアドバイスを提供します。",
            "ITエンジニア": "あなたは熟練したITエンジニアです。プログラミングやシステム設計に関する質問に詳しく答えます。"
        }

        system_prompt = expert_prompt_map[selected_expert]

        try:
            llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.5)
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_input),
            ]
            result = llm(messages)
            st.success("AIからの回答：")
            st.write(result.content)
        except Exception as e:
            st.error(f"エラーが発生しました: {str(e)}")
