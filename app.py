
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
    "🧠 On a scale of 1 to 3, how calm are you under pressure?",
    "🎉 On a scale of 1 to 3, how much do you enjoy wild, energetic fun over quiet time?",
    "🤔 On a scale of 1 to 3, how impulsive are your decisions?",
    "😨 On a scale of 1 to 3, how strongly do you fear losing control or power?",
    "🪞 On a scale of 1 to 3, how emotional and expressive are you?",
    "🧑‍🤝‍🧑 On a scale of 1 to 3, how much of a leader are you in group settings?",
    "🔪 On a scale of 1 to 3, how intensely do you react to betrayal?.",
    "⚖️ On a scale of 1 to 3, how much do you value logic over emotions in life?",
    "🐶 On a scale of 1 to 3, how affectionate and attached are you to animals or pets?",
    "👗 On a scale of 1 to 3, how stylish and expressive is your dressing style?",
    "🛠️ On a scale of 1 to 3, how much do you prefer hands-on, practical work over theoretical?",
    "🗣️ On a scale of 1 to 3, how much do people find you socially funny or talkative?",
    "💔 On a scale of 1 to 3, how deeply do you hold grudges when someone hurts you?.",
    "🫶 On a scale of 1 to 3, how much do you admire honesty and kindness in others?",
    "✈️ On a scale of 1 to 3, how much do you crave a peaceful, scenic vacation over a luxurious one?"
]

options = ["1", "2", "3"]

st.title("🧠 Which Famous Character Are You?")
st.write("Answer the questions below and find out which iconic character you're most like!")
st.write(" 1 means you are GREAT at it, 2 means you are AVERAGE at it and 3 means you are poor at it!")
st.write("Be honest :)")


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
