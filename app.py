import streamlit as st
import joblib
import numpy as np
import os
import requests # Used for downloading images
from pathlib import Path # For better path manipulation

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

# Set Streamlit page configuration (must be called once at the top of the script)
st.set_page_config(page_title="Which Famous Character Are You?", layout="centered")

# --- Background Color Management ---
# Define a default background color for the app's initial state.
# This color is chosen to be clearly non-white and provide good contrast for questions.
DEFAULT_BACKGROUND_COLOR = "#2c3e50" # Dark slate grey/charcoal
DEFAULT_TEXT_COLOR = "white" # Text color for default dark background

# Function to set dynamic background color for the whole app
def set_background_color(hex_color, text_color):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {hex_color};
            color: {text_color}; /* Set text color based on background for readability */
        }}
        /* Ensure specific elements like headers and bold text also inherit or have good contrast */
        h1, h2, h3, h4, h5, h6, strong {{
            color: {text_color};
        }}
        /* For the selectbox labels which are bold markdown */
        .stSelectbox label p strong {{
            color: {text_color};
        }}
        /* Text inputs and other elements might need specific styling if they don't inherit well */
        div[data-testid="stTextInput"] > label > div > p,
        div[data-testid="stTextarea"] > label > div > p {{
            color: {text_color};
        }}
        /* General paragraph text */
        .stMarkdown p {{
            color: {text_color};
        }}
        </style>
        """,
        unsafe_allow_html=True # Required to inject custom HTML/CSS
    )

# Dictionary mapping characters to their specific background colors.
# Most of these are light, so we'll set their text color to black.
color_map = {
    "Walter White": {"bg": "#F4D03F", "text": "black"},  # Yellowish
    "Michael Scott": {"bg": "#D6EAF8", "text": "black"}, # Light Blue
    "Nezuko": {"bg": "#F9EBEA", "text": "black"},      # Light Pink/Beige
    "Sheldon Cooper": {"bg": "#E8DAEF", "text": "black"}, # Light Purple
    "Johan Liebert": {"bg": "#FADBD8", "text": "black"},  # Light Peach
    "Moira Rose": {"bg": "#FCF3CF", "text": "black"},    # Creamy Yellow
    "Phil Dunphy": {"bg": "#D1F2EB", "text": "black"},    # Light Teal
    "Cameron Tucker": {"bg": "#FADBD8", "text": "black"}, # Light Peach
    "Ron Swanson": {"bg": "#FDEDEC", "text": "black"},    # Light Red/Orange
    "Sherlock Holmes": {"bg": "#EAECEE", "text": "black"},# Light Grey
    "Batman": {"bg": "#D5DBDB", "text": "black"},       # Grey
    "Peter Griffin": {"bg": "#F6DDCC", "text": "black"},  # Light Orange
    "Daenerys": {"bg": "#EBDEF0", "text": "black"},     # Lavender
    "Andy Dwyer": {"bg": "#FEF9E7", "text": "black"},    # Pale Yellow
    "Jethalal Gada": {"bg": "#FCF3CF", "text": "black"}, # Creamy Yellow
    "Chandler Bing": {"bg": "#E8F8F5", "text": "black"}  # Mint Green
}

# Base URL for the raw images on GitHub
GITHUB_IMAGES_BASE_URL = "[https://raw.githubusercontent.com/Anni3607/Personality-Traits/main/images/](https://raw.githubusercontent.com/Anni3607/Personality-Traits/main/images/)"

# Cache the downloaded images locally to avoid re-downloading on every run
@st.cache_resource
def download_image(character_name):
    """
    Downloads an image from GitHub to a local temporary directory
    and returns its local path.
    """
    # Construct the image filename based on character name and .png extension
    image_filename = f"{character_name.replace(' ', '_').lower()}.png"
    remote_image_url = GITHUB_IMAGES_BASE_URL + image_filename

    # --- FIX for AttributeError: Using a stable, relative path for cached downloads ---
    # Get the directory where the current script (app.py) is located
    current_script_dir = Path(__file__).parent
    # Define a subfolder within the script's directory for downloaded images
    download_dir = current_script_dir / "temp_downloaded_images"
    
    # Create the directory if it doesn't exist
    download_dir.mkdir(parents=True, exist_ok=True)
    local_image_path = download_dir / image_filename

    if not local_image_path.exists():
        try:
            st.info(f"Downloading image for {character_name}...") # Informative message
            response = requests.get(remote_image_url, stream=True)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

            with open(local_image_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            st.success(f"Successfully downloaded {image_filename}!")
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to download image for {character_name} from {remote_image_url}: {e}")
            return None # Return None if download fails
    return str(local_image_path) # Return the string path

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

# Options for the selectbox inputs
options = ["1", "2", "3"]

# --- Streamlit UI Layout ---

# Apply the initial default background and text color when the app first loads
set_background_color(DEFAULT_BACKGROUND_COLOR, DEFAULT_TEXT_COLOR)

st.title("🧠 Which Famous Character Are You?")
st.write("Answer the questions below and find out which iconic character you're most like!")
st.write("1 means you are GREAT at it, 2 means you are AVERAGE at it and 3 means you are poor at it!")
st.write("Be honest :)")

answers = []
for idx, question in enumerate(questions):
    answer = st.selectbox(f"**{question}**", options, key=idx)
    answers.append(int(answer))

# Button to trigger the character prediction
if st.button("✨ Reveal Your Character"):
    input_data = np.array(answers).reshape(1, -1)
    prediction = model.predict(input_data)
    character = le.inverse_transform(prediction)[0]

    colors = color_map.get(character, {"bg": DEFAULT_BACKGROUND_COLOR, "text": DEFAULT_TEXT_COLOR})
    set_background_color(colors["bg"], colors["text"])
    
    st.subheader(f"🎉 You are most like **{character}**!")

    # Attempt to download the image locally
    local_image_path = download_image(character)
    
    if local_image_path:
        # Use st.image() with the local path
        st.image(local_image_path, caption=character, use_container_width=True)
    else:
        # Fallback if download fails (e.g., show a placeholder or message)
        st.warning(f"Could not load image for {character}. Displaying placeholder.")
        # Show placeholder HTML for more control
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; margin-bottom: 10px;">
                <img src="[https://placehold.co/300x300/cccccc/ffffff?text=Image+Missing](https://placehold.co/300x300/cccccc/ffffff?text=Image+Missing)" 
                     alt="Image for {character} not found" 
                     style="max-width: 100%; height: auto; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.2); 
                            background-color: #f0f0f0; padding: 10px; border: 1px solid #ddd;">
            </div>
            <p style="text-align: center; font-size: 1.2em; font-weight: bold;">{character}</p>
            """,
            unsafe_allow_html=True
        )

