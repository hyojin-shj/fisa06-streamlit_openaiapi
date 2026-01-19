# 1. 가상환경 생성 0
# 2. 필요한 패키지 설치 0
# 3. streamlit input / output 만들기  0
# 4. p실제 local 서버에서 실행되는지 확인
# 4-1. pip freeze > requirements.txt0
# 4-2. .gitignore 작성해서 .env 가리기0
# 5. github repo 만들기0
# 6. share.streamlit.io에 연동하기

import os
from openai import OpenAI
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

@st.cache_data
def load_data():
    df = pd.read_excel(r'Adidas US Sales Datasets.xlsx', skiprows=4)
    return df

df = load_data()

def table_definition_prompt(df):
    prompt = '''Given the following pandas dataframe definition,
            write queries based on the request
            \n### pandas dataframe, with its properties:

            #
            # df의 컬럼명({})
            #
            '''.format(",".join(str(x) for x in df.columns))

    return prompt

#streamlit 인풋
st.title('DF 어시스턴트')
user_input = st.text_input('질문을 입력하세요:')


client = OpenAI(api_key=api_key)

response = client.responses.create(
    model="gpt-5-nano",
    input=[
            {"role": "system", "content": "You are an assistant that generates Pandas boolean indexing code based on the given df definition\
            and a natural language request. The answer should start with df and contains only code by one line, not any explanation or ``` for copy."},
            {"role": "user", "content": f"A query to answer: {table_definition_prompt(df) + user_input}"}
        ]
)

st.write(eval(response.output_text))