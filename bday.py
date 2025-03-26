import streamlit as st
import requests

# -------------------------
# Gemini API text generation
# -------------------------
def generate_text(prompt):
    api_key = "AIzaSyCr8niD4_LvntSAdd8apKnFC9uMZK5WeNU"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        candidates = result.get("candidates", [])
        if candidates and candidates[0].get("content", {}).get("parts"):
            return candidates[0]["content"]["parts"][0]["text"]
        else:
            return "Hmm, I couldn't generate a dynamic response."
    except Exception as e:
        return f"[Error with Gemini API: {e}]"

# -------------------------
# Define game scenes
# -------------------------
SCENES = [
    {
        "title": "Welcome to the Journey!",
        "text": ("Hello, adventurer! Today you embark on a wild journey across a fantastical land. "
                 "Your mission: reach the mystical City of Joy and celebrate your special day with epic cheer. "
                 "Press 'Start' to begin your adventure."),
        "choices": {"Start": 1}
    },
    {
        "title": "The Enchanted Forest",
        "text": (
            "You enter a vibrant forest filled with glowing flora and quirky creatures. "
            "As you walk, you notice a strange gadget lying on the forest floor—a device that "
            "converts trash into dazzling art. \n\n"
            "Gemini says: " + generate_text("Give a funny compliment on inventing a gadget that turns trash into art") +
            "\n\nWhat do you do?"
        ),
        "choices": {
            "Pick up the gadget": 2,
            "Leave it and explore deeper": 3
        }
    },
    {
        "title": "Gadget Genius",
        "text": (
            "You pick up the gadget and, with your inventive spirit, start tinkering with it. "
            "Miraculously, the gadget starts transforming discarded plastic into vibrant sculptures! "
            "The forest creatures cheer and dance around you. \n\n"
            "Gemini adds: " + generate_text("A witty remark about turning trash into art") +
            "\n\nFeeling inspired, you continue on your journey."
        ),
        "choices": {"Continue": 4}
    },
    {
        "title": "Mystic River",
        "text": (
            "Further along, you arrive at a shimmering river that flows with recycled magic. "
            "There, you can choose to either help clean the river or simply take a moment to reflect "
            "by its banks. \n\n"
            "Gemini notes: " + generate_text("A humorous observation about cleaning a magical river") +
            "\n\nWhat will you do?"
        ),
        "choices": {
            "Help clean the river": 5,
            "Sit and reflect": 6
        }
    },
    {
        "title": "The City of Joy",
        "text": (
            "After a long journey filled with wonder and quirky choices, you finally arrive at the City of Joy. "
            "The streets are vibrant, music fills the air, and people are celebrating life. \n\n"
            "A wise, friendly bot appears at the central plaza..."
        ),
        "choices": {"Meet the Bot": 7}
    },
    {
        "title": "River Revival",
        "text": (
            "Rolling up your sleeves, you dive into the task of cleaning the river. "
            "Working together with locals and enchanted creatures, you turn the murky water clear, "
            "unleashing a burst of rainbow light. \n\n"
            "Gemini says: " + generate_text("A humorous remark about reviving a magical river") +
            "\n\nFeeling fulfilled, you resume your journey."
        ),
        "choices": {"Continue": 4}
    },
    {
        "title": "Moment of Reflection",
        "text": (
            "You take a quiet moment by the river, gazing at your reflection and feeling the gentle breeze. "
            "This pause fills you with clarity and creative energy. \n\n"
            "Gemini adds: " + generate_text("A light-hearted joke about the power of reflection") +
            "\n\nRefreshed, you get back on the path."
        ),
        "choices": {"Continue": 4}
    },
    {
        "title": "The Grand Finale",
        "text": (
            "At last, you reach the heart of the City of Joy. A cheerful bot awaits you in a plaza adorned "
            "with balloons and streamers. With a warm smile, the bot says:\n\n"
            "'Happy Birthday, adventurer! May your journey be filled with laughter, creativity, and endless joy. "
            "Your spirit lights up the world—keep shining!'\n\n"
            "Your adventure has reached a joyful conclusion."
        ),
        "choices": {}
    }
]

# -------------------------
# Session State & Navigation
# -------------------------
if "scene" not in st.session_state:
    st.session_state.scene = 0

def go_to_scene(scene_index):
    st.session_state.scene = scene_index

# -------------------------
# Main UI
# -------------------------
st.title("Adventurer's Journey")

current_scene = SCENES[st.session_state.scene]
st.header(current_scene["title"])
st.write(current_scene["text"])

if current_scene["choices"]:
    for label, next_scene in current_scene["choices"].items():
        if st.button(label):
            go_to_scene(next_scene)
else:
    st.write("The journey is complete. Enjoy your special day!")
