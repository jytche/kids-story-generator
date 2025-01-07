import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("Disney-themed bedtime story generator")
st.subheader("Create magical bedtime stories for your little ones!")

character = st.text_input("Main Character","a kind princess named Charlotte")
setting = st.text_input("Setting","a magical forest")
lesson = st.text_input("Moral Lesson","kindness")
custom_element = st.text_input("Custom Element", "a magical key")

if "story" not in st.session_state:
    st.session_state.story = ""

if st.button("Generate story!"):
    with st.spinner("Generating your magical bedtime story..."):
       messages = [
            {
                "role": "system",
                "content": "You are a creative storyteller who writes heartwarming, Disney-style bedtime stories for children."
            },
            {
                "role": "user",
                "content": f"Write a bedtime story where the main character is {character}, set in {setting}. "
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
            st.markdown(st.session_state.story)
    except Exception as e:
            st.error(f"An error occurred: {e}")

if st.session_state.story and st.button("Listen to Story"):
    with st.spinner("Now narrating your story..."):
        try:
                response = client.audio.speech.create(
                   model="tts-1",
                   voice="alloy",
                   input=st.session_state.story)
                response.stream_to_file("output.mp3")
                st.audio("output.mp3", format="audio/mp3")
        except Exception as e:
             st.error(f"An error occurred: {e}")
elif not st.session_state.story:
    st.warning("Please generate a story first!")