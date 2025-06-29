import streamlit as st
import joblib
import numpy as np
# from PIL import Image # PIL (Pillow) is not directly used for st.image, so it can be commented out if not needed elsewhere

# Load the trained model and label encoder
# Ensure these files ('character_predictor.pkl', 'label_encoder.pkl') are in the same directory
# as app.py or in a correctly specified relative path on your deployment platform.
try:
    model = joblib.load("character_predictor.pkl")
    le = joblib.load("label_encoder.pkl")
except FileNotFoundError as e:
    st.error(f"Error loading model or label encoder: {e}. Please ensure 'character_predictor.pkl' and 'label_encoder.pkl' are in the correct path.")
    st.stop() # Stop the app if essential files are missing

# Set Streamlit page configuration
st.set_page_config(page_title="Which Famous Character Are You?", layout="centered")

# Function to set dynamic background color based on prediction
def set_background_color(hex_color):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {hex_color};
            color: black; /* Ensure text remains visible against varying backgrounds */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Dictionary mapping characters to background colors
color_map = {
    "Walter White": "#F4D03F",  # Yellowish
    "Michael Scott": "#D6EAF8", # Light Blue
    "Nezuko": "#F9EBEA",      # Light Pink/Beige
    "Sheldon Cooper": "#E8DAEF", # Light Purple
    "Johan Liebert": "#FADBD8",  # Light Peach
    "Moira Rose": "#FCF3CF",    # Creamy Yellow
    "Phil Dunphy": "#D1F2EB",    # Light Teal
    "Cameron Tucker": "#FADBD8", # Light Peach
    "Ron Swanson": "#FDEDEC",    # Light Red/Orange
    "Sherlock Holmes": "#EAECEE",# Light Grey
    "Batman": "#D5DBDB",       # Grey
    "Peter Griffin": "#F6DDCC",  # Light Orange
    "Daenerys": "#EBDEF0",     # Lavender
    "Andy Dwyer": "#FEF9E7",    # Pale Yellow
    "Jethalal Gada": "#FCF3CF", # Creamy Yellow
    "Chandler Bing": "#E8F8F5"  # Mint Green
}

# Function to generate the correct raw GitHub image URL
def get_image_path(character):
    # Construct the file name based on the character name.
    # Replace spaces with underscores and convert to lowercase, then add .jpg extension.
    # This assumes your image files on GitHub follow this naming convention.
    image_filename = f"{character.replace(' ', '_').lower()}.jpg"
    # Use the raw.githubusercontent.com URL for direct image access
    # Ensure 'Anni3607', 'Personality-Traits', and 'main' match your GitHub repo details
    return f"[https://raw.githubusercontent.com/Anni3607/Personality-Traits/main/images/](https://raw.githubusercontent.com/Anni3607/Personality-Traits/main/images/){image_filename}"

# Define the questions for the personality quiz
questions = [
    "🧠 On a scale of 1 to 3, how calm are you under pressure?",
    "🎉 On a scale of 1 to 3, how much do you enjoy wild, energetic fun over quiet time?",
    "🤔 On a scale of 1 to 3, how impulsive are your decisions?",
    "😨 On a scale of 1 to 3, how strongly do you fear losing control or power?",
    "🪞 On a scale of 1 to 3, how emotional and expressive are you?",
    "🧑‍🤝‍🧑 On a scale of 1 to 3, how much of a leader are you in group settings?",
    "🔪 On a scale of 1 to 3, how intensely do you react to betrayal?", # Corrected punctuation
    "⚖️ On a scale of 1 to 3, how much do you value logic over emotions in life?",
    "🐶 On a scale of 1 to 3, how affectionate and attached are you to animals or pets?",
    "👗 On a scale of 1 to 3, how stylish and expressive is your dressing style?",
    "🛠️ On a scale of 1 to 3, how much do you prefer hands-on, practical work over theoretical?",
    "🗣️ On a scale of 1 to 3, how much do people find you socially funny or talkative?",
    "💔 On a scale of 1 to 3, how deeply do you hold grudges when someone hurts you?", # Corrected punctuation
    "🫶 On a scale of 1 to 3, how much do you admire honesty and kindness in others?",
    "✈️ On a scale of 1 to 3, how much do you crave a peaceful, scenic vacation over a luxurious one?"
]

# Options for the selectbox inputs
options = ["1", "2", "3"]

# Streamlit UI elements for the quiz introduction
st.title("🧠 Which Famous Character Are You?")
st.write("Answer the questions below and find out which iconic character you're most like!")
st.write("1 means you are GREAT at it, 2 means you are AVERAGE at it and 3 means you are poor at it!")
st.write("Be honest :)")

answers = []
for idx, question in enumerate(questions):
    # Display each question using st.selectbox for user input
    answer = st.selectbox(f"**{question}**", options, key=idx)
    answers.append(int(answer)) # Convert answer to integer and store

# Button to trigger character prediction
if st.button("✨ Reveal Your Character"):
    # Convert list of answers to a numpy array and reshape for model prediction
    input_data = np.array(answers).reshape(1, -1)
    
    # Make prediction using the loaded model
    prediction = model.predict(input_data)
    
    # Inverse transform the numerical prediction back to character name using label encoder
    character = le.inverse_transform(prediction)[0]

    # Set background color based on the predicted character
    set_background_color(color_map.get(character, "#FFFFFF")) # Default to white if character not in map
    
    # Display the prediction result
    st.subheader(f"🎉 You are most like **{character}**!")

    # Get the correct image URL for the predicted character
    image_url = get_image_path(character)
    
    # Display the character image.
    # Changed 'use_column_width=True' to 'use_container_width=True' to fix deprecation warning.
    # 'use_container_width' makes the image fill the width of its parent container.
    st.image(image_url, caption=character, use_container_width=True)

