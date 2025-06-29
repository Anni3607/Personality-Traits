import streamlit as st
import joblib
import numpy as np
# from PIL import Image # PIL (Pillow) is not directly used for st.image, so it can be commented out if not needed elsewhere

# Load the trained model and label encoder
# IMPORTANT: Ensure these files ('character_predictor.pkl', 'label_encoder.pkl')
# are in the same directory as app.py on your deployment platform (e.g., GitHub repo).
try:
    model = joblib.load("character_predictor.pkl")
    le = joblib.load("label_encoder.pkl")
except FileNotFoundError as e:
    st.error(f"Error loading model or label encoder: {e}. "
             "Please ensure 'character_predictor.pkl' and 'label_encoder.pkl' "
             "are in the correct path on your deployment server.")
    st.stop() # Stop the app execution if essential files are missing

# Set Streamlit page configuration (must be called once at the top)
st.set_page_config(page_title="Which Famous Character Are You?", layout="centered")

# Define a default background color for the app's initial state
# This will be applied before any prediction is made.
DEFAULT_BACKGROUND_COLOR = "#E0F7FA" # A pleasant light blue/cyan shade

# Function to set dynamic background color for the whole app
def set_background_color(hex_color):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {hex_color};
            color: black; /* Keep text color black for readability against varying backgrounds */
        }}
        </style>
        """,
        unsafe_allow_html=True # Required to inject custom HTML/CSS
    )

# Dictionary mapping characters to their specific background colors
# These colors will be applied after a character is predicted.
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
# This is crucial for images hosted on GitHub to display correctly in deployed apps.
# It points to the raw content, not the GitHub web page view.
def get_image_path(character):
    # Ensure the character name matches the image file naming convention.
    # e.g., "Walter White" -> "walter_white.jpg"
    image_filename = f"{character.replace(' ', '_').lower()}.jpg"
    # IMPORTANT: Verify 'Anni3607', 'Personality-Traits', and 'main'
    # match your exact GitHub username, repository name, and branch name.
    return f"[https://raw.githubusercontent.com/Anni3607/Personality-Traits/main/images/](https://raw.githubusercontent.com/Anni3607/Personality-Traits/main/images/){image_filename}"

# Define the questions for the personality quiz
questions = [
    "🧠 On a scale of 1 to 3, how calm are you under pressure?",
    "🎉 On a scale of 1 to 3, how much do you enjoy wild, energetic fun over quiet time?",
    "🤔 On a scale of 1 to 3, how impulsive are your decisions?",
    "😨 On a scale of 1 to 3, how strongly do you fear losing control or power?",
    "🪞 On a scale of 1 to 3, how emotional and expressive are you?",
    "🧑‍🤝‍🧑 On a scale of 1 to 3, how much of a leader are you in group settings?",
    "🔪 On a scale of 1 to 3, how intensely do you react to betrayal?",
    "⚖️ On a scale of 1 to 3, how much do you value logic over emotions in life?",
    "🐶 On a scale of 1 to 3, how affectionate and attached are you to animals or pets?",
    "👗 On a scale of 1 to 3, how stylish and expressive is your dressing style?",
    "🛠️ On a scale of 1 to 3, how much do you prefer hands-on, practical work over theoretical?",
    "🗣️ On a scale of 1 to 3, how much do people find you socially funny or talkative?",
    "💔 On a scale of 1 to 3, how deeply do you hold grudges when someone hurts you?",
    "🫶 On a scale of 1 to 3, how much do you admire honesty and kindness in others?",
    "✈️ On a scale of 1 to 3, how much do you crave a peaceful, scenic vacation over a luxurious one?"
]

# Options for the selectbox inputs (remains "1", "2", "3")
options = ["1", "2", "3"]

# --- Streamlit UI Layout ---

# Apply the initial default background color when the app first loads
set_background_color(DEFAULT_BACKGROUND_COLOR)

st.title("🧠 Which Famous Character Are You?")
st.write("Answer the questions below and find out which iconic character you're most like!")
st.write("1 means you are GREAT at it, 2 means you are AVERAGE at it and 3 means you are poor at it!")
st.write("Be honest :)")

answers = []
for idx, question in enumerate(questions):
    # Display each question using st.selectbox for user input
    answer = st.selectbox(f"**{question}**", options, key=idx)
    answers.append(int(answer)) # Convert selected option to integer

# Button to trigger the character prediction
if st.button("✨ Reveal Your Character"):
    # Prepare input data for the model
    input_data = np.array(answers).reshape(1, -1)
    
    # Make prediction using the loaded model
    prediction = model.predict(input_data)
    
    # Inverse transform the numerical prediction back to the character name
    character = le.inverse_transform(prediction)[0]

    # Dynamically set the background color based on the predicted character
    # If a character is not in the color_map, it will default to DEFAULT_BACKGROUND_COLOR
    set_background_color(color_map.get(character, DEFAULT_BACKGROUND_COLOR))
    
    # Display the prediction result
    st.subheader(f"🎉 You are most like **{character}**!")

    # Get the correctly formatted image URL for the predicted character
    image_url = get_image_path(character)
    
    # --- IMPORTANT FIX FOR IMAGE DISPLAY ---
    # Instead of st.image(), we use st.markdown() with an <img> tag.
    # This directly embeds the image URL into the HTML, bypassing Streamlit's
    # internal media file manager which seems to be causing the error by
    # attempting to read the URL as a local file.
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; margin-bottom: 10px;">
            <img src="{image_url}" alt="{character}" style="max-width: 100%; height: auto; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
        </div>
        <p style="text-align: center; font-size: 1.2em; font-weight: bold;">{character}</p>
        """,
        unsafe_allow_html=True # Crucial for rendering HTML tags
    )

    # Optional: Add a check if the image URL is valid (can be complex to do reliably client-side)
    # For now, relying on the correct URL generation and GitHub's reliability.

