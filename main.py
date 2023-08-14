import os
import streamlit as st
from langchain.llms import OpenAI
from textwrap import dedent

st.title("Twice Unrelated")
st.subheader("See how seemingly unrelated things are related")

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password") or os.environ.get("OPENAI_API_KEY", "")
st.sidebar.write("This API key will not be persisted anywhere")

def generate_response(input_text):
    llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key, model_name="gpt-4")
    prompt_prefix = """let's play a game where i'll list two seemingly
    unrelated comma separated concepts and you tell me a creative way in which
    they are related. the relationship should not be something mundane like
    about people or places, but something intellectually stimulating. for
    example, "x and y were invented by hungarians" is lot less interesting than
    "x and y both reveal underlying reality of natural numbers". be concise and
    succinct.

    your response should have two parts. first part should be a one word
    summary. second part should be three paragraphs of interesting explanation.
    these two parts should be separated by |. do not under any circumstances
    deviate from this output format. """
    prompt = f"{dedent(prompt_prefix)}\n{input_text}"
    return llm(prompt)

def split_response(response):
    print(response)
    parsed = response.split("|", 1)
    if len(parsed) != 2:
        parsed = response.split(" ", 1)
    if len(parsed) != 2:
        return ["Error", "Error parsing response"]

    relation = parsed[0].strip()
    relation = "".join(e for e in relation if e.isalnum() or e == " ")
    body = parsed[1].strip()
    return [relation, body]

def render_response(items):
    st.info(f"{items[0]}")
    st.info(f"{items[1]}")

with st.form("my_form"):
    st.info("Enter two unrelated things:")
    text1 = st.text_input("First Thing", value="loretz attractors", max_chars=40)
    text2 = st.text_input("Second Thing", value="flatworms", max_chars=40)
    submitted = st.form_submit_button("Submit")
    if not openai_api_key.startswith("sk-"):
        st.warning("Enter your OpenAI API key in the sidebar", icon="⚠")
    if submitted and openai_api_key.startswith("sk-"):
        text = f"{text1.replace(',', ' ')}, {text2.replace(',', ' ')}".strip()
        r = generate_response(text)
        ht = split_response(r)
        render_response(ht)
