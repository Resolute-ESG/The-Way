import streamlit as st
import openai
from datetime import datetime
import os
import json
import calendar

# Set your OpenAI API key securely (e.g. via environment variable)
openai.api_key = os.getenv("OPENAI_API_KEY")

# File to store reflections in structured format
REFLECTIONS_FILE = "reflections.json"

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
    except Exception as e:
        return f"[Error generating response: {e}]"

def generate_prompt():
    today = datetime.today().strftime('%Y-%m-%d')

    try:
        morning = call_genai(
            "Write a short morning intention in the voice of 'The Way of the Resolute'—calm, clear, and focused on soul alignment."
        )

        mantra = call_genai(
            "Create a poetic, one-sentence mantra in the tone of 'The Way of the Resolute'. Must feel spiritual and grounded."
        )

        action = call_genai(
            "Suggest one small, soul-aligned action someone can take today to feel empowered and present. Write in an inspiring tone."
        )

        reflection = call_genai(
            "Offer a single evening reflection question that helps someone reconnect with themselves after a long day."
        )

        # Check for fallback trigger
        if '[Error' in morning or '[Error' in mantra or '[Error' in action or '[Error' in reflection:
            raise Exception("Fallback to static prompts")

    except Exception:
        # Fallback values drawn from previously generated Way of the Resolute prompts
        from random import choice

        static_morning = [
            "Today, I open with calm and rise with quiet confidence.",
            "I begin with a soft heart and an anchored spirit.",
            "I walk through this day with reverence and resolve.",
            "I rise in peace, not perfection.",
            "Today, I move with the grace of one who has already returned home.",
            "I don’t chase. I allow. I receive.",
            "This day does not own me—I move through it with quiet strength."
        ]

        static_mantras = [
            "I align with the power of Source. I am receiving. I am home.",
            "With every breath, I rise into who I was meant to be.",
            "Stillness is my power, truth is my direction.",
            "I am not striving—I am returning.",
            "What is for me already knows my name.",
            "My grounded presence is my greatest strength.",
            "I will not shrink—I was born to expand."
        ]

        static_actions = [
            "Speak one truth you've been holding inside.",
            "Create a sacred pause in your schedule today.",
            "Offer a word of kindness, even if unspoken aloud.",
            "Write a single sentence that reminds you who you are.",
            "Make one decision today from your higher self, not your habits.",
            "Breathe deeply before responding—choose intention over reaction.",
            "Say no without guilt, yes without fear."
        ]

        static_reflections = [
            "Where did I move from love today?",
            "What did I release that no longer served me?",
            "Did I show up in alignment with my deepest values?",
            "Where did I feel most myself?",
            "What moment reminded me of my strength?",
            "What am I still carrying that I can now set down?",
            "Did I honour my boundaries and my breath today?"
        ]

        morning = choice(static_morning)
        mantra = choice(static_mantras)
        action = choice(static_actions)
        reflection = choice(static_reflections)

    return {
        "date": today,
        "morning_intention": morning,
        "mantra": mantra,
        "aligned_action": action,
        "evening_reflection": reflection
    }

def save_reflection(date, content):
    reflections = load_all_reflections()
    reflections[date] = content
    with open(REFLECTIONS_FILE, "w") as f:
        json.dump(reflections, f, indent=4)

def load_all_reflections():
    if os.path.exists(REFLECTIONS_FILE):
        with open(REFLECTIONS_FILE, "r") as f:
            return json.load(f)
    return {}

# Streamlit UI
st.set_page_config(page_title="The Ready Soul", layout="centered")
st.title("🌿 The Ready Soul – Daily Manifestation")

st.markdown("---")

# Display today's prompt
prompt = generate_prompt()

st.subheader(f"🗓️ Daily Guidance – {prompt['date']}")
st.markdown(f"**🌞 Morning Intention:** {prompt['morning_intention']}")
st.markdown(f"**🔮 Mantra:** {prompt['mantra']}")
st.markdown(f"**🌱 Aligned Action:** {prompt['aligned_action']}")
st.markdown(f"**🌙 Evening Reflection:** {prompt['evening_reflection']}\n")

# Journaling Section
st.markdown("---")
st.subheader("📓 Reflection Journal")

journal_entry = st.text_area("Write your thoughts, intentions, or reflections here:")

if st.button("Save Reflection"):
    if journal_entry.strip():
        save_reflection(prompt['date'], journal_entry.strip())
        st.success("Reflection saved.")
    else:
        st.warning("Please write something before saving.")

# Calendar-style Reflection Viewer with edit option
st.markdown("---")
st.subheader("📅 Calendar View: Review & Edit Reflections")
all_reflections = load_all_reflections()
if all_reflections:
    dates = sorted(all_reflections.keys(), reverse=True)
    selected_date = st.date_input("Select a date to view or edit:", datetime.today())
    selected_str = selected_date.strftime('%Y-%m-%d')

    if selected_str in all_reflections:
        edited_entry = st.text_area(f"Reflection on {selected_str}", value=all_reflections[selected_str], height=200)
        if st.button("Update Reflection"):
            save_reflection(selected_str, edited_entry.strip())
            st.success("Reflection updated.")
    else:
        st.info("No reflection saved for this date.")
else:
    st.info("No reflections saved yet. Start by writing your first one today!")

# Regenerate Prompt
st.markdown("---")
if st.button("🔁 Regenerate Today's Prompt"):
    try:
        st.experimental_rerun()
    except Exception:
        st.warning("Regenerated Scroll to the Top to see your new 🌞 Morning Intention: 🔮 Mantra: 🌱 Aligned Action: 
🌙 Evening Reflection:")
