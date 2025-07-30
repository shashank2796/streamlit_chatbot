# from openai import OpenAI 
import os
# Disable proxy variables if they exist
# os.environ["HTTP_PROXY"] = "http://your.proxy.com:port"
# os.environ["HTTPS_PROXY"] = "http://your.proxy.com:port"
import openai
from dotenv import load_dotenv
import base64
import streamlit as st
load_dotenv()
# api_key = os.getenv("OPENAI_API_KEY")

# client = OpenAI(api_key=api_key)

openai.api_key = st.secrets["OPENAI_API_KEY"]

# api_key = st.secrets["OPENAI_API_KEY"]
# client = OpenAI(api_key=api_key)

def get_answer(messages):
    system_message = [{"role": "system", "content": "You are a helpful AI chatbot that answers questions asked by the User."}]
    messages = system_message + messages
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages
    )
    return response.choices[0].message.content

def speech_to_text(audio_data):
    with open(audio_data, "rb") as audio_file:
        transcript = openai.audio.transcriptions.create(
            model="whisper-1",
            response_format="text",
            file=audio_file
        )
    return transcript

def text_to_speech(input_text):
    response = openai.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=input_text
    )
    webm_file_path = "temp_audio_play.mp3"
    with open(webm_file_path, "wb") as f:
        response.stream_to_file(webm_file_path)
    return webm_file_path

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    md = f"""
    <audio autoplay=>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>"""
    
    st.markdown(md, unsafe_allow_html=True)
