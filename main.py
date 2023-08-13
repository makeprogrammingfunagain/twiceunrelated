import os
import streamlit as st
from langchain.llms import OpenAI
from textwrap import dedent

st.title("Stretch Your Imagination")

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password") or os.environ.get("OPENAI_API_KEY", "")

def generate_response(input_text):
    llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
    prompt_prefix = """ let's play a game where i'll list two seemingly
    unrelated concepts and you tell me a creative way in which they are related.
    the relationship should not be something mundane like about people or
    places, but something intellectually stimulating. for example, "x and y were
    invented by hungarians" is lot less interesting than "x and y both reveal
    underlying reality of prime numbers. be concise and succinct. please start
    with a one word summary of the conceptual relationship. this one word
    summary should be the very first word in the response, in a line by itself.
    then after a blank line, go into three paragraphs of explanation."

    """
    prompt = f"{dedent(prompt_prefix)}\n{input_text}"
    st.info(llm(prompt))

with st.form("my_form"):
    text = st.text_input("Enter two unrelated things:", value="loretz attractors and flatworms", max_chars=80)
    submitted = st.form_submit_button("Submit")
    if not openai_api_key.startswith("sk-"):
        st.warning("Enter your OpenAI API key", icon="⚠")
    if submitted and openai_api_key.startswith("sk-"):
        generate_response(text)
