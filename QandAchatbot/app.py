import streamlit as st
import openai
import os
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from dotenv import load_dotenv
loader=load_dotenv()


os.environ["LANGCHAIN_API_KEY"]=os.getenv('LANGCHAIN_API_KEY')
os.environ["LANGCHAIN_TRACKNG_V2"]='true'
os.environ["LANGCHAIN_PROJECT"]="Q and A Chantbot with OpenAI"

prompt=ChatPromptTemplate.from_messages(
    [
        ("system","Please give answer to the user queries"),
        ("user","Question:{question}")
    ]
)

def generate_response(question,api_key,llm,temperature,max_tokens):
    openai.api_key=api_key
    llm=ChatOpenAI(model=llm)
    outputparser=StrOutputParser()
    chain=prompt|llm|outputparser
    answer=chain.invoke({'question':question})
    return answer



""" Streamlit Setup for userinterface UI"""

st.title("Enhanced Q and A chatbot with OpenAI")
st.sidebar.title("Settings")
api_key=st.sidebar.text_input("Enter your open_api_key:", type="password")
llm = st.sidebar.selectbox("Select an OpenAI model", ["gpt-4o", "gpt-4-turbo", "gpt-4"])
temperature=st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)
max_tokens=st.sidebar.slider("Max_tokens",min_value=50,max_value=300,value=150)


st.write("Please Go ahead and ask your Question")
user_input=st.text_input("You:")
if user_input:
    response=generate_response(user_input,api_key,llm,temperature,max_tokens)
    st.write(response)
else:
    st.write("Please provide Query")

