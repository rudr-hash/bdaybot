import streamlit as st
import requests
import time

# -------------------------
# Function to generate dynamic text messages
# -------------------------
def generate_text(prompt, max_retries=3, backoff_factor=2):
    api_key = "AIzaSyCr8niD4_LvntSAdd8apKnFC9uMZK5WeNU"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    for attempt in range(max_retries):
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            candidates = result.get("candidates", [])
            if candidates and candidates[0].get("content", {}).get("parts"):
                return candidates[0]["content"]["parts"][0]["text"]
            else:
                return "Hmm, no message generated."
        elif response.status_code == 429:
            wait_time = backoff_factor ** attempt
            st.warning(f"Rate limit reached. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        else:
            return f"Error {response.status_code}: {response.text}"
    return "[Error: Rate limit exceeded]"

# -------------------------
# Define game scenes around wishing Nayantara Happy Birthday
# -------------------------
SCENES = [
    {
        "title": "Welcome, Nayantara!",
        "text": (
            "Happy Birthday, Nayantara! Today, you embark on a magical journey through memories and moments "
            "that have defined your incredible path. Your mission is to rediscover the joy of your past and embrace "
            "the bright future ahead. Press 'Begin' to start your adventure."
        ),
        "choices": {"Begin": 1}
    },
    {
        "title": "The Memory Forest",
        "text": (
            "You wander into a forest where every tree whispers a memory. Along the winding path, you discover a "
            "mysterious gadget lying beneath an ancient oak—a relic from your past that once sparked your creativity.\n\n"
            "Nayantara from the past says: " + generate_text("Provide a nostalgic compliment on discovering a magical gadget from your youth for your birthday") +
            "\n\nWhat do you do?"
        ),
        "choices": {
            "Pick up the gadget": 2,
            "Leave it and wander further": 3
        }
    },
    {
        "title": "Gadget of Memories",
        "text": (
            "You pick up the gadget, and as you examine it, memories of youthful adventures flood back. "
            "The gadget miraculously transforms everyday discarded items into sparkling works of art, as if "
            "reminiscent of the dreams you once had.\n\n"
            "Nayantara from the past adds: " + generate_text("Share a witty, heartfelt remark about transforming everyday moments into art for your birthday") +
            "\n\nInspired, you continue your journey."
        ),
        "choices": {"Continue": 4}
    },
    {
        "title": "The Mystic River of Time",
        "text": (
            "Further along your path, you encounter a shimmering river that flows with the energy of past laughter and "
            "joy. You sense that this river holds the power to refresh your spirit.\n\n"
            "Nayantara from the past observes: " + generate_text("Offer a humorous yet reflective comment about the healing power of memories and time on your birthday") +
            "\n\nWhat will you do?"
        ),
        "choices": {
            "Help cleanse the river": 5,
            "Sit and reflect by the water": 6
        }
    },
    {
        "title": "City of Celebrations",
        "text": (
            "Your journey brings you to a vibrant city pulsing with celebration. Streets are lined with confetti, "
            "music fills the air, and joyful voices echo in every corner. Here, the spirit of your past and present "
            "converges in a dazzling festival."
        ),
        "choices": {"Proceed to the Grand Finale": 7}
    },
    {
        "title": "River Revival",
        "text": (
            "Rolling up your sleeves, you join the locals in cleansing the mystical river. Together, you restore its "
            "sparkling clarity, releasing a burst of rainbow light that rekindles your inner spark.\n\n"
            "Nayantara from the past remarks: " + generate_text("A humorous note on how reviving a river is like reviving old joyful memories on your birthday") +
            "\n\nFeeling rejuvenated, you continue."
        ),
        "choices": {"Continue": 4}
    },
    {
        "title": "Moment of Reflection",
        "text": (
            "You pause by the river, taking a quiet moment to reflect on your journey so far. The gentle breeze and "
            "the soft murmur of water remind you of the laughter and love from days gone by.\n\n"
            "Nayantara from the past chimes in: " + generate_text("A light-hearted joke about cherishing the sweet moments of life on your birthday") +
            "\n\nRefreshed, you rise to continue your journey."
        ),
        "choices": {"Continue": 4}
    },
    {
        "title": "The Grand Finale",
        "text": (
            "At last, you arrive in the central plaza of the City of Celebrations. A warm, friendly bot greets you, "
            "its voice imbued with the wisdom of years past.\n\n"
            "'Happy Birthday, Nayantara! Today, you have not only celebrated another year but also rediscovered the magic "
            "of your journey. May your memories inspire your future and your heart always remain young and full of joy.'\n\n"
            "Your adventure concludes with a celebration of you—past, present, and future."
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
st.title("Nayantara's Birthday Journey")

current_scene = SCENES[st.session_state.scene]
st.header(current_scene["title"])
st.write(current_scene["text"])

if current_scene["choices"]:
    for label, next_scene in current_scene["choices"].items():
        if st.button(label):
            go_to_scene(next_scene)
            # The state update will trigger a rerun, no explicit st.experimental_rerun() needed.
else:
    st.write("The journey is complete. Enjoy your special day!")
