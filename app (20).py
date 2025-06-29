import streamlit as st
import joblib
import numpy as np
# Removed 'from PIL import Image' as it's not used in this final version.

# --- Model and Label Encoder Loading ---
# Ensure 'character_predictor.pkl' and 'label_encoder.pkl' are in the same directory
# as app.py in your GitHub repository for deployment.
try:
    model = joblib.load("character_predictor.pkl")
    le = joblib.load("label_encoder.pkl")
except FileNotFoundError as e:
    st.error(f"Initialization Error: Required model files not found. "
             f"Please ensure 'character_predictor.pkl' and 'label_encoder.pkl' "
             f"are in the root of your GitHub repository. Error: {e}")
    st.stop() # Stop the app if essential files are missing

# --- Page Configuration ---
st.set_page_config(page_title="Which Famous Character Are You?", layout="centered")

# --- Background and Text Color Management ---
# Default background color for the app's initial state and as a fallback.
# Chosen for good contrast with white text.
DEFAULT_BACKGROUND_COLOR = "#2c3e50" # Dark charcoal
DEFAULT_TEXT_COLOR = "white"

# Function to dynamically set the background and text colors of the entire app.
def set_background_color(bg_hex_color, text_hex_color):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {bg_hex_color};
            color: {text_hex_color}; /* Sets default text color for the app */
        }}
        /* Ensure key elements like headers and strong text maintain good contrast */
        h1, h2, h3, h4, h5, h6, strong {{
            color: {text_hex_color};
        }}
        /* Specifically target selectbox labels, which are rendered as markdown p strong */
        .stSelectbox label p strong {{
            color: {text_hex_color};
        }}
        /* General paragraph text */
        .stMarkdown p {{
            color: {text_hex_color};
        }}
        /* Any other specific elements that need color adjustment */
        </style>
        """,
        unsafe_allow_html=True # Required to inject custom CSS
    )

# Dictionary mapping characters to their specific background and text colors.
# Most character-specific backgrounds are light, so their text is black.
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

# --- Image Handling with GitHub Pages ---
# This is the most reliable way to serve images directly from your GitHub repo.
# YOU MUST SET UP GITHUB PAGES FOR YOUR REPOSITORY.
# Base URL for images served via GitHub Pages.
# Replace 'Anni3607' with your GitHub username and 'Personality-Traits' with your repository name.
# Ensure your 'images' folder is directly in the root of your 'main' branch on GitHub.
GITHUB_PAGES_BASE_URL = "[https://annni3607.github.io/Personality-Traits/images/](https://annni3607.github.io/Personality-Traits/images/)"

# Function to generate the correct GitHub Pages image URL.
# It assumes image files are lowercase with underscores and have a .png extension.
def get_image_url(character):
    # Example: "Sheldon Cooper" -> "sheldon_cooper.png"
    image_filename = f"{character.replace(' ', '_').lower()}.png"
    return GITHUB_PAGES_BASE_URL + image_filename

# --- Questions and Options ---
questions_and_choices = [
    {
        "question": "🧠 On a scale of 1 to 3, how calm are you under pressure?",
        "options": ["Very calm", "Moderately calm", "Easily stressed"]
    },
    {
        "question": "🎉 On a scale of 1 to 3, how much do you enjoy wild, energetic fun over quiet time?",
        "options": ["Love it (wild fun)", "Balanced", "Prefer quiet time"]
    },
    {
        "question": "🤔 On a scale of 1 to 3, how impulsive are your decisions?",
        "options": ["Very impulsive", "Moderately impulsive", "Thoughtful and planned"]
    },
    {
        "question": "😨 On a scale of 1 to 3, how strongly do you fear losing control or power?",
        "options": ["Very strongly", "Moderately", "Not much"]
    },
    {
        "question": "🪞 On a scale of 1 to 3, how emotional and expressive are you?",
        "options": ["Very expressive", "Moderately expressive", "Reserved"]
    },
    {
        "question": "🧑‍🤝‍🧑 On a scale of 1 to 3, how much of a leader are you in group settings?",
        "options": ["Strong leader", "Sometimes lead", "Prefer to follow"]
    },
    {
        "question": "🔪 On a scale of 1 to 3, how intensely do you react to betrayal?",
        "options": ["Very intensely", "Moderately", "Calmly"]
    },
    {
        "question": "⚖️ On a scale of 1 to 3, how much do you value logic over emotions in life?",
        "options": ["Highly value logic", "Balanced", "Highly value emotions"]
    },
    {
        "question": "🐶 On a scale of 1 to 3, how affectionate and attached are you to animals or pets?",
        "options": ["Very affectionate", "Moderately", "Not very affectionate"]
    },
    {
        "question": "👗 On a scale of 1 to 3, how stylish and expressive is your dressing style?",
        "options": ["Very stylish", "Moderately stylish", "Practical and simple"]
    },
    {
        "question": "🛠️ On a scale of 1 to 3, how much do you prefer hands-on, practical work over theoretical?",
        "options": ["Strongly prefer hands-on", "Balanced", "Strongly prefer theoretical"]
    },
    {
        "question": "🗣️ On a scale of 1 to 3, how much do people find you socially funny or talkative?",
        "options": ["Very funny/talkative", "Moderately", "Quiet/reserved"]
    },
    {
        "question": "💔 On a scale of 1 to 3, how deeply do you hold grudges when someone hurts you?",
        "options": ["Very deeply", "Moderately", "Easily forgive"]
    },
    {
        "question": "🫶 On a scale of 1 to 3, how much do you admire honesty and kindness in others?",
        "options": ["Highly admire", "Moderately", "Less of a priority"]
    },
    {
        "question": "✈️ On a scale of 1 to 3, how much do you crave a peaceful, scenic vacation over a luxurious one?",
        "options": ["Peaceful, scenic", "Balanced", "Luxurious"]
    }
]


# --- Streamlit UI Layout ---

# Apply the initial default background and text color when the app first loads
set_background_color(DEFAULT_BACKGROUND_COLOR, DEFAULT_TEXT_COLOR)

st.title("🧠 Which Famous Character Are You?")
st.write("Answer the questions below and find out which iconic character you're most like!")
st.write("For each question, choose the option that best describes you.")
st.write("Be honest :)")

answers = []
for idx, q_data in enumerate(questions_and_choices):
    # Using specific options for each question for better user experience
    answer = st.selectbox(f"**{q_data['question']}**", q_data['options'], key=idx)
    # Convert the selected option back to numerical value (1, 2, or 3)
    # The index is 0-based, so add 1 to get 1, 2, or 3.
    answers.append(q_data['options'].index(answer) + 1)

# Button to trigger character prediction
if st.button("✨ Reveal Your Character"):
    # Ensure all questions are answered before proceeding
    if len(answers) != len(questions_and_choices):
        st.error("Please answer all questions before revealing your character.")
    else:
        # Prepare input data for the model prediction
        input_data = np.array(answers).reshape(1, -1)
        
        try:
            # Make prediction using the loaded model
            prediction = model.predict(input_data)
            # Inverse transform the numerical prediction back to the character name
            character = le.inverse_transform(prediction)[0]
        except Exception as e:
            st.error(f"Prediction Error: Could not predict character. "
                     "Please check if your model ('character_predictor.pkl') "
                     f"and label encoder ('label_encoder.pkl') are valid. Error details: {e}")
            # Optionally, you might want to st.stop() here in a real app,
            # but for debugging, letting it continue might show other issues.

        # Get specific background and text colors for the predicted character
        # Fallback to default colors if character not found in color_map
        colors = color_map.get(character, {"bg": DEFAULT_BACKGROUND_COLOR, "text": DEFAULT_TEXT_COLOR})
        set_background_color(colors["bg"], colors["text"])
        
        # Display the prediction result
        st.subheader(f"🎉 You are most like **{character}**!")

        # Get the image URL using the function defined above (GitHub Pages)
        image_url = get_image_url(character)
        
        # --- IMAGE DISPLAY ---
        # Using st.markdown() with an <img> HTML tag for direct browser loading.
        # This method is robust as it bypasses Streamlit's internal media handling.
        # The 'onerror' attribute provides a client-side fallback if the image URL fails to load.
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

