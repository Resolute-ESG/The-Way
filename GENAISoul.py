import streamlit as st
import openai
from datetime import datetime
import os
import json

# Set your OpenAI API key securely (e.g. via environment variable)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Check for missing API key and display helpful error
if not openai.api_key:
    st.error("🔑 OpenAI API key is not set. Please add it to your environment or Streamlit secrets.")
    st.stop()

# Fallback values from The Way of the Resolute
from random import choice

static_morning = [
    "Today, I open with calm and rise with quiet confidence.",
    "I begin with a soft heart and an anchored spirit.",
    "I walk through this day with reverence and resolve.",
    "I rise in peace, not perfection.",
    "Today, I move with the grace of one who has already returned home.",
    "I don’t chase. I allow. I receive.",
    "This day does not own me—I move through it with quiet strength.",
    "I am not attached to the outcome—I am anchored in who I am becoming.",
    "Even when inspiration is absent, I become it.",
    "Today I will show them how it should and could be."
]

static_mantras = [
    "I align with the power of Source. I am receiving. I am home.",
    "With every breath, I rise into who I was meant to be.",
    "Stillness is my power, truth is my direction.",
    "I am not striving—I am returning.",
    "What is for me already knows my name.",
    "My grounded presence is my greatest strength.",
    "I will not shrink—I was born to expand.",
    "I have dug the foundations. I have laid the path. Now—I walk.",
    "I do not chase, cling or force. I trust the unfolding.",
    "I move with intention, speak with clarity, and hold space for wonder."
]

static_actions = [
    "Speak one truth you've been holding inside.",
    "Create a sacred pause in your schedule today.",
    "Offer a word of kindness, even if unspoken aloud.",
    "Write a single sentence that reminds you who you are.",
    "Make one decision today from your higher self, not your habits.",
    "Breathe deeply before responding—choose intention over reaction.",
    "Say no without guilt, yes without fear.",
    "Rest as an act of resistance."
]

static_reflections = [
    "Where did I move from love today?",
    "What did I release that no longer served me?",
    "Did I show up in alignment with my deepest values?",
    "Where did I feel most myself?",
    "What moment reminded me of my strength?",
    "What am I still carrying that I can now set down?",
    "Did I honour my boundaries and my breath today?",
    "Where did I support change without needing to control it?",
    "What was whispering to me today that I chose to hear?",
    "What did I learn by not reacting?"
]

def call_genai(prompt, system="You are a soulful guide helping users live with clarity and courage. Use poetic language."):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return None

def generate_prompt():
    today = datetime.today().strftime('%Y-%m-%d')
    morning = call_genai("Write a short morning intention in the voice of 'The Way of the Resolute'.") or choice(static_morning)
    mantra = call_genai("Create a poetic, one-sentence mantra in the tone of 'The Way of the Resolute'.") or choice(static_mantras)
    action = call_genai("Suggest one small, soul-aligned action someone can take today.") or choice(static_actions)
    reflection = call_genai("Offer an evening reflection question.") or choice(static_reflections)
    return {
        "date": today,
        "morning_intention": morning,
        "mantra": mantra,
        "aligned_action": action,
        "evening_reflection": reflection
    }

# Streamlit UI
st.set_page_config(page_title="The Ready Soul", layout="centered")
st.title("🌿 The Ready Soul – Daily Manifestation")

st.markdown("---")
prompt = generate_prompt()

st.subheader(f"🗓️ Daily Guidance – {prompt['date']}")
st.markdown(f"**🌞 Morning Intention:** {prompt['morning_intention']}")
st.markdown(f"**🔮 Mantra:** {prompt['mantra']}")
st.markdown(f"**🌱 Aligned Action:** {prompt['aligned_action']}")
st.markdown(f"**🌙 Evening Reflection:** {prompt['evening_reflection']}")

st.markdown("---")
st.info("📝 Reflections are now local only and will not be stored or recalled. For privacy and simplicity, journaling is a personal practice in the moment.")
