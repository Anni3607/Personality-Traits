
import streamlit as st
import joblib
import numpy as np
from PIL import Image

model = joblib.load("character_predictor.pkl")
le = joblib.load("label_encoder.pkl")

st.set_page_config(page_title="Which Famous Character Are You?", layout="centered")

def set_background_color(hex_color):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {hex_color};
            color: black;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

color_map = {
    "Walter White": "#F4D03F",
    "Michael Scott": "#D6EAF8",
    "Nezuko": "#F9EBEA",
    "Sheldon Cooper": "#E8DAEF",
    "Johan Liebert": "#FADBD8",
    "Moira Rose": "#FCF3CF",
    "Phil Dunphy": "#D1F2EB",
    "Cameron Tucker": "#FADBD8",
    "Ron Swanson": "#FDEDEC",
    "Sherlock Holmes": "#EAECEE",
    "Batman": "#D5DBDB",
    "Peter Griffin": "#F6DDCC",
    "Daenerys": "#EBDEF0",
    "Andy Dwyer": "#FEF9E7",
    "Jethalal Gada": "#FCF3CF",
    "Chandler Bing": "#E8F8F5"
}

def get_image_path(character):
    return f"https://github.com/Anni3607/Personality-Traits/tree/main/images{character.replace(' ', '_').lower()}.jpg"

questions = [
    "How do you handle pressure?",
    "What's your idea of fun?",
    "How do you usually make decisions?",
    "What's your biggest fear?",
    "What describes your personality best?",
    "What's your role in a group?",
    "If betrayed, you would...",
    "What's more important to you?",
    "Which pet would you choose?",
    "Your dressing style is?",
    "You prefer work that is...",
    "People often describe you as...",
    "When someone hurts you, you...",
    "What do you value most in others?",
    "What’s your dream vacation?"
]

options = ["1", "2", "3"]

st.title("🧠 Which Famous Character Are You?")
st.write("Answer the questions below and find out which iconic character you're most like!")

answers = []
for idx, question in enumerate(questions):
    answer = st.selectbox(f"**{question}**", options, key=idx)
    answers.append(int(answer))

if st.button("✨ Reveal Your Character"):
    input_data = np.array(answers).reshape(1, -1)
    prediction = model.predict(input_data)
    character = le.inverse_transform(prediction)[0]

    set_background_color(color_map.get(character, "#FFFFFF"))
    st.subheader(f"🎉 You are most like **{character}**!")

    image_url = get_image_path(character)
    st.image(image_url, caption=character, use_column_width=True)
