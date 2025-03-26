import streamlit as st
import requests

# Function to call the Gemini API and generate dynamic text.
def generate_text(prompt):
    # Replace with your actual Gemini API endpoint
    api_url = "https://gemini.googleapis.com/v1/generateText"
    headers = {"Authorization": f"Bearer AIzaSyCr8niD4_LvntSAdd8apKnFC9uMZK5WeNU"}
    data = {
        "prompt": prompt,
        "max_tokens": 100  # Adjust as needed
    }
    try:
        response = requests.post(api_url, json=data, headers=headers)
        response.raise_for_status()
        generated = response.json().get("generated_text", "")
    except Exception as e:
        generated = f"[Error with Gemini API: {e}]"
    return generated

# Define the adventure storyline as a list of scenes
SCENES = [
    {
        "title": "The Beginning",
        "text": "Welcome, Nayantara! Today is a very special day—your birthday! Your journey begins in a lush, eco-friendly forest where every leaf recycles itself. The gentle hum of nature welcomes you. Are you ready to begin your adventure?",
        "choices": {"Start": 1}
    },
    {
        "title": "The Eco-Quest",
        "text": "You come across a shimmering river with a twist: it flows with recycled energy. A sign reads: 'Choose your destiny.' Do you:",
        "choices": {
            "Invent a gadget that turns plastic into art": 2,
            "Devise a plan to clean the river": 3,
            "Sit and enjoy the moment with a cup of organic coffee": 4
        }
    },
    {
        "title": "Gadget Genius",
        "text": "Your inventive spirit shines as you design a quirky device that transforms plastic waste into beautiful sculptures. The forest creatures applaud your creativity. (Gemini says: " + generate_text("funny compliment on inventing eco-gadgets") + ")",
        "choices": {"Continue": 5}
    },
    {
        "title": "River Revival",
        "text": "With determination, you rally the local community to clean the river, turning pollution into pure energy. Your eco-heroism is unmatched. (Gemini notes: " + generate_text("witty remark about cleaning rivers") + ")",
        "choices": {"Continue": 5}
    },
    {
        "title": "Moment of Zen",
        "text": "You take a moment to relax by the river, sipping your organic coffee. The calm instills a sense of creative wonder. (Gemini adds: " + generate_text("a light-hearted joke about enjoying nature") + ")",
        "choices": {"Continue": 5}
    },
    {
        "title": "The Grand Finale",
        "text": "Your journey has led you to a magical clearing where the wise bot awaits. The bot greets you with a warm smile and says: 'Happy Birthday, Nayantara! May your ideas flourish like the greenest gardens and your laughter light up every corner of the world!'",
        "choices": {}
    }
]

# Initialize session state for scene tracking
if "scene" not in st.session_state:
    st.session_state.scene = 0

def go_to_scene(scene_index):
    st.session_state.scene = scene_index

# Main UI
st.title("Nayantara's Birthday Journey")

current_scene = SCENES[st.session_state.scene]

st.header(current_scene["title"])
st.write(current_scene["text"])

if current_scene["choices"]:
    for choice_text, next_scene in current_scene["choices"].items():
        if st.button(choice_text):
            go_to_scene(next_scene)
            # Only call experimental_rerun if available
            if hasattr(st, "experimental_rerun"):
                st.experimental_rerun()
else:
    st.write("The journey is complete. Enjoy your special day!")
