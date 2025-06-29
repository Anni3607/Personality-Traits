import streamlit as st
import joblib
import numpy as np

# Load the trained model and label encoder
try:
    model = joblib.load("character_predictor.pkl")
    le = joblib.load("label_encoder.pkl")
except FileNotFoundError as e:
    st.error(f"Error loading model or label encoder: {e}. "
             "Please ensure 'character_predictor.pkl' and 'label_encoder.pkl' "
             "are in the correct path on your deployment server.")
    st.stop()

# Set Streamlit page configuration
st.set_page_config(page_title="Which Famous Character Are You?", layout="centered")

# --- Background Color Management ---
DEFAULT_BACKGROUND_COLOR = "#2c3e50" # Dark slate grey/charcoal
DEFAULT_TEXT_COLOR = "white" # Text color for default dark background

def set_background_color(hex_color, text_color):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {hex_color};
            color: {text_color}; /* Set text color based on background for readability */
        }}
        h1, h2, h3, h4, h5, h6, strong {{
            color: {text_color};
        }}
        .stSelectbox label p strong {{
            color: {text_color};
        }}
        div[data-testid="stTextInput"] > label > div > p,
        div[data-testid="stTextarea"] > label > div > p {{
            color: {text_color};
        }}
        .stMarkdown p {{
            color: {text_color};
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

color_map = {
    "Walter White": {"bg": "#F4D03F", "text": "black"},
    "Michael Scott": {"bg": "#D6EAF8", "text": "black"},
    "Nezuko": {"bg": "#F9EBEA", "text": "black"},
    "Sheldon Cooper": {"bg": "#E8DAEF", "text": "black"},
    "Johan Liebert": {"bg": "#FADBD8", "text": "black"},
    "Moira Rose": {"bg": "#FCF3CF", "text": "black"},
    "Phil Dunphy": {"bg": "#D1F2EB", "text": "black"},
    "Cameron Tucker": {"bg": "#FADBD8", "text": "black"},
    "Ron Swanson": {"bg": "#FDEDEC", "text": "black"},
    "Sherlock Holmes": {"bg": "#EAECEE", "text": "black"},
    "Batman": {"bg": "#D5DBDB", "text": "black"},
    "Peter Griffin": {"bg": "#F6DDCC", "text": "black"},
    "Daenerys": {"bg": "#EBDEF0", "text": "black"},
    "Andy Dwyer": {"bg": "#FEF9E7", "text": "black"},
    "Jethalal Gada": {"bg": "#FCF3CF", "text": "black"},
    "Chandler Bing": {"bg": "#E8F8F5", "text": "black"}
}

# --- IMAGE HANDLING SECTION ---
# CHOOSE ONE of the two options below based on where you host your images:
#
# OPTION 1: If using Imgur, Cloudinary, etc., where each image has a unique URL:
IMAGE_URLS = {
    "Walter White": "[https://placehold.co/300x300/F4D03F/black?text=Walter+White](https://placehold.co/300x300/F4D03F/black?text=Walter+White)", # Replace with actual Imgur/Cloudinary URL
    "Michael Scott": "[https://placehold.co/300x300/D6EAF8/black?text=Michael+Scott](https://placehold.co/300x300/D6EAF8/black?text=Michael+Scott)",
    "Nezuko": "[https://placehold.co/300x300/F9EBEA/black?text=Nezuko](https://placehold.co/300x300/F9EBEA/black?text=Nezuko)",
    "Sheldon Cooper": "[https://placehold.co/300x300/E8DAEF/black?text=Sheldon+Cooper](https://placehold.co/300x300/E8DAEF/black?text=Sheldon+Cooper)", # YOUR NEW URL HERE
    "Johan Liebert": "[https://placehold.co/300x300/FADBD8/black?text=Johan+Liebert](https://placehold.co/300x300/FADBD8/black?text=Johan+Liebert)",
    "Moira Rose": "[https://placehold.co/300x300/FCF3CF/black?text=Moira+Rose](https://placehold.co/300x300/FCF3CF/black?text=Moira+Rose)",
    "Phil Dunphy": "[https://placehold.co/300x300/D1F2EB/black?text=Phil+Dunphy](https://placehold.co/300x300/D1F2EB/black?text=Phil+Dunphy)",
    "Cameron Tucker": "[https://placehold.co/300x300/FADBD8/black?text=Cameron+Tucker](https://placehold.co/300x300/FADBD8/black?text=Cameron+Tucker)",
    "Ron Swanson": "[https://placehold.co/300x300/FDEDEC/black?text=Ron+Swanson](https://placehold.co/300x300/FDEDEC/black?text=Ron+Swanson)",
    "Sherlock Holmes": "[https://placehold.co/300x300/EAECEE/black?text=Sherlock+Holmes](https://placehold.co/300x300/EAECEE/black?text=Sherlock+Holmes)",
    "Batman": "[https://placehold.co/300x300/D5DBDB/black?text=Batman](https://placehold.co/300x300/D5DBDB/black?text=Batman)",
    "Peter Griffin": "[https://placehold.co/300x300/F6DDCC/black?text=Peter+Griffin](https://placehold.co/300x300/F6DDCC/black?text=Peter+Griffin)",
    "Daenerys": "[https://placehold.co/300x300/EBDEF0/black?text=Daenerys](https://placehold.co/300x300/EBDEF0/black?text=Daenerys)",
    "Andy Dwyer": "[https://placehold.co/300x300/FEF9E7/black?text=Andy+Dwyer](https://placehold.co/300x300/FEF9E7/black?text=Andy+Dwyer)",
    "Jethalal Gada": "[https://placehold.co/300x300/FCF3CF/black?text=Jethalal+Gada](https://placehold.co/300x300/FCF3CF/black?text=Jethalal+Gada)",
    "Chandler Bing": "[https://placehold.co/300x300/E8F8F5/black?text=Chandler+Bing](https://placehold.co/300x300/E8F8F5/black?text=Chandler+Bing)",
}

def get_image_url(character):
    return IMAGE_URLS.get(character, "[https://placehold.co/300x300/cccccc/ffffff?text=Image+URL+Missing](https://placehold.co/300x300/cccccc/ffffff?text=Image+URL+Missing)")

# OR
#
# OPTION 2: If you set up GitHub Pages for your repository:
# GITHUB_PAGES_BASE_URL = "[https://annni3607.github.io/Personality-Traits/images/](https://annni3607.github.io/Personality-Traits/images/)"
#
# def get_image_url(character):
#     image_filename = f"{character.replace(' ', '_').lower()}.png"
#     return GITHUB_PAGES_BASE_URL + image_filename
#
# --- END OF IMAGE HANDLING SECTION ---


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

options = ["1", "2", "3"]

# --- Streamlit UI Layout ---
set_background_color(DEFAULT_BACKGROUND_COLOR, DEFAULT_TEXT_COLOR)

st.title("🧠 Which Famous Character Are You?")
st.write("Answer the questions below and find out which iconic character you're most like!")
st.write("1 means you are GREAT at it, 2 means you are AVERAGE at it and 3 means you are poor at it!")
st.write("Be honest :)")

answers = []
for idx, question in enumerate(questions):
    answer = st.selectbox(f"**{question}**", options, key=idx)
    answers.append(int(answer))

if st.button("✨ Reveal Your Character"):
    input_data = np.array(answers).reshape(1, -1)
    prediction = model.predict(input_data)
    character = le.inverse_transform(prediction)[0]

    colors = color_map.get(character, {"bg": DEFAULT_BACKGROUND_COLOR, "text": DEFAULT_TEXT_COLOR})
    set_background_color(colors["bg"], colors["text"])
    
    st.subheader(f"🎉 You are most like **{character}**!")

    # Get the image URL using the function defined above
    image_url = get_image_url(character)
    
    # --- IMAGE DISPLAY ---
    # Using st.markdown() with an <img> tag for direct browser loading.
    # Added onerror to show a placeholder if the image fails to load from the URL.
    st.markdown(
        f"""
        <div style="display: flex; justify-content: center; margin-bottom: 10px;">
            <img src="{image_url}" 
                 alt="Image for {character} not found" 
                 style="max-width: 100%; height: auto; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);"
                 onerror="this.onerror=null;this.src='[https://placehold.co/300x300/cccccc/ffffff?text=Image+Missing](https://placehold.co/300x300/cccccc/ffffff?text=Image+Missing)';">
        </div>
        <p style="text-align: center; font-size: 1.2em; font-weight: bold;">{character}</p>
        """,
        unsafe_allow_html=True
    )

