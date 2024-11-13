from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model=genai.GenerativeModel("gemini-pro")
chat=model.start_chat(history=[])

def get_gemini_response(question):
    response=chat.send_message(question,stream=True)
    return response

st.set_page_config(page_title="Q&A Demo")
st.header("Gemini LLM Application")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history']=[]

input=st.text_input("Input: ", key="input")
submit=st.button("Ask the question")

if submit and input:
    response = get_gemini_response(input)
    st.session_state['chat_history'].append(("User", input))
    st.subheader("The response is: ")
    try:
        for chunk in response:
            if hasattr(chunk, 'text'):
                st.write(chunk.text)
                st.session_state['chat_history'].append(("Bot", chunk.text))
            else:
                error_message = "Sorry, I couldn't process that request. It may contain copyrighted material."
                st.error(error_message)
                st.session_state['chat_history'].append(("Bot", error_message))
                break
    except ValueError as e:
        error_message = "An error occurred while processing your request."
        st.error(error_message)
        st.session_state['chat_history'].append(("Bot", error_message))

st.subheader("The Chat History is")

for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")