import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="Story Maker", layout="wide")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("Themed story maker")
st.subheader("Create magical stories for your little ones!")

col1, col2, col3, col4 = st.columns([2,0.2,3,0.2])

with col1:
    character = st.text_input("👸  This story will star the character(s):","Charlotte, a kind princess")
    setting = st.text_input("🌳  And set in:","a magical forest")
    lesson = st.text_input("📚  With a moral lesson about:","kindness")
    custom_element = st.text_input("🔑  And include a special surprise of:", "a magical key")
    theme = st.text_input("✨  Themes:", "Disney")
    
    if "story" not in st.session_state:
        st.session_state.story = ""
    
    col1, col2 = st.columns([1,1])

    with col1:
        create_button = st.button("🪄 Create your story!")
    with col2:
        narrate_button = st.button("🎵 Narrate your story!")

with col3:

    if create_button:
        with st.spinner("Now creating your story..."):
           messages = [
                {
                    "role": "system",
                    "content": "You are a creative storyteller who writes heartwarming, Disney-style stories for children between the ages of 3 and 8. These stories can be narrated under 5 minutes."
                },
                {
                    "role": "user",
                    "content": f"Write a bedtime story where the characters are {character}, set in {setting} in the style of {theme}."
                               f"The story should teach a moral lesson about {lesson} and include {custom_element}."
                }
            ]

        try:
                response = client.chat.completions.create(model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=1000,
                temperature=0.7)

                st.session_state.story = response.choices[0].message.content
                st.success("Heres your story!")  
        except Exception as e:
                st.error(f"An error occurred: {e}")

    if st.session_state.story:
        st.markdown(st.session_state.story)

if narrate_button:
    if st.session_state.story:
        with st.spinner("Now narrating your story..."):
            try:
                    response = client.audio.speech.create(
                       model="tts-1",
                       voice="alloy",
                       input=st.session_state.story)
                    response.stream_to_file("output.mp3")
                    st.audio("output.mp3", format="audio/mp3")
            except Exception as e:
                  st.error(f"An error occurred: ")
    else:
         st.warning("Please create a story first!")