import streamlit as st
import requests
import time

# -------------------------
# Function to generate dynamic text messages with retry logic
# -------------------------
def generate_text(prompt, max_retries=3, backoff_factor=2):
    api_key = "AIzaSyCr8niD4_LvntSAdd8apKnFC9uMZK5WeNU"
    # Using the Vertex AI REST endpoint for Gemini 2.0 Flash (v1beta)
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
# Game Scenes Definition
# -------------------------
# Each scene is a dictionary with a title, text, and choices mapping to the next scene index.
SCENES = [
    {
        "title": "Welcome, Nayantara!",
        "text": (
            "Happy Birthday, Nayantara! Today you embark on a magical journey to relive your cherished memories "
            "and embrace a bright future. Your adventure begins now—press 'Begin Adventure' to start."
        ),
        "choices": {"Begin Adventure": 1}
    },
    {
        "title": "Memory Forest",
        "text": (
            "You wander into a lush forest where every tree whispers a memory. You spot a curious gadget lying under an ancient oak—"
            "a relic from your past that once ignited your creativity.\n\n"
            "Nayantara from the past says: " + generate_text("Offer a nostalgic compliment about discovering a magical gadget in your youth for your birthday") +
            "\n\nWhat will you do?"
        ),
        "choices": {
            "Pick up the gadget": 2,
            "Keep walking deeper": 3
        }
    },
    {
        "title": "Gadget of Memories",
        "text": (
            "You pick up the gadget and begin to tinker with it. Almost magically, it transforms discarded plastic into dazzling sculptures, "
            "reminiscent of the dreams and ambitions of your younger days.\n\n"
            "Nayantara from the past adds: " + generate_text("Share a witty remark on turning everyday discarded items into works of art on your birthday") +
            "\n\nInspired, you move on."
        ),
        "choices": {"Continue": 4}
    },
    {
        "title": "Mystic River of Time",
        "text": (
            "Further along, you come upon a shimmering river that flows with the essence of past laughter and joy. "
            "The water glows with memories of celebrations long ago.\n\n"
            "Nayantara from the past observes: " + generate_text("Make a humorous yet heartfelt comment about the healing power of memories flowing like a river") +
            "\n\nDo you:"
        ),
        "choices": {
            "Help cleanse the river": 5,
            "Sit and reflect by the river": 6
        }
    },
    {
        "title": "River Revival",
        "text": (
            "Rolling up your sleeves, you help cleanse the river alongside cheerful locals and enchanted creatures. "
            "As the murky water turns crystal clear, a burst of rainbow light revives your spirit.\n\n"
            "Nayantara from the past remarks: " + generate_text("Say something humorous about how reviving a river is like rejuvenating old memories on your birthday") +
            "\n\nFeeling renewed, you continue your journey."
        ),
        "choices": {"Continue": 4}
    },
    {
        "title": "Moment of Reflection",
        "text": (
            "You pause at the riverbank, taking a quiet moment to reflect on all the wonderful memories and dreams that have shaped you. "
            "The gentle breeze and soft murmur of the water fill you with warmth.\n\n"
            "Nayantara from the past chimes in: " + generate_text("Give a light-hearted joke about cherishing memories and staying young at heart on your birthday") +
            "\n\nRecharged, you get back on the path."
        ),
        "choices": {"Continue": 4}
    },
    {
        "title": "City of Celebrations",
        "text": (
            "You finally arrive at a dazzling city pulsing with festivity. The streets are alive with music, laughter, and vibrant colors. "
            "In the heart of the city, the spirit of your past and the promise of the future merge into a grand celebration."
        ),
        "choices": {"Proceed to the Finale": 7}
    },
    {
        "title": "Grand Finale",
        "text": (
            "At the central plaza of the City of Celebrations, a friendly, wise bot greets you with a radiant smile:\n\n"
            "'Happy Birthday, Nayantara! Today you have journeyed through memories and moments, rediscovering the magic within. "
            "May your future be as bright and joyful as your spirit, and may your heart always be full of wonder!'\n\n"
            "Your adventure comes to a joyful close."
        ),
        "choices": {}
    }
]

# -------------------------
# Chat History Setup for Extra Interactivity
# -------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def add_chat_message(role, message):
    st.session_state.chat_history.append((role, message))

# -------------------------
# Session State for Scene Navigation
# -------------------------
if "scene" not in st.session_state:
    st.session_state.scene = 0

def go_to_scene(scene_index):
    st.session_state.scene = scene_index

# -------------------------
# Layout: Choose Adventure Mode or Chat Mode
# -------------------------
st.sidebar.title("Modes")
mode = st.sidebar.radio("Select Mode", options=["Adventure", "Chat"])

if mode == "Adventure":
    st.title("Nayantara's Birthday Adventure")
    
    current_scene = SCENES[st.session_state.scene]
    st.header(current_scene["title"])
    st.write(current_scene["text"])
    
    if current_scene["choices"]:
        for label, next_scene in current_scene["choices"].items():
            if st.button(label):
                go_to_scene(next_scene)
                # State change automatically triggers rerun
    else:
        st.write("The adventure is complete. Enjoy your special day!")
    
elif mode == "Chat":
    st.title("Chat with Nayantara from the Past")
    
    st.write("Type your message below to chat with a version of Nayantara from your past. "
             "She will respond with memories and wisdom from days gone by.")
    
    # Display chat history
    for role, message in st.session_state.chat_history:
        if role == "user":
            st.markdown(f"**You:** {message}")
        else:
            st.markdown(f"**Nayantara (past):** {message}")
    
    user_input = st.text_input("Your message", key="chat_input")
    if st.button("Send"):
        if user_input:
            add_chat_message("user", user_input)
            # Use the generation API to get a response tailored to chat context
            chat_prompt = f"As Nayantara from the past, reply warmly to: {user_input}"
            response = generate_text(chat_prompt)
            add_chat_message("bot", response)
            st.experimental_rerun()  # Force update of chat history
