import streamlit as st
import random
from datetime import datetime

# Sample content pools
morning_intentions = [
    "Today, I walk in alignment. I choose clarity, lead with kindness, welcome fun, and trust my path.",
    "I begin this day open to the magic of becoming. I choose to respond, not react.",
    "My energy is sacred. I move only in ways that honor my becoming."
]

aligned_actions = [
    "Say no to something that no longer feels aligned.",
    "Do one thing just for fun—sing, dance, laugh.",
    "Reach out to someone who brings light into your life."
]

evening_reflections = [
    "Where did I feel most like myself today?",
    "What small moment brought me joy today?",
    "Did I choose courage over comfort today?"
]

# Modular mantra generation
mantra_starts = [
    "Today, I rise in",
    "With every breath, I embrace",
    "I align myself with",
    "I choose to walk in"
]

mantra_themes = [
    "clarity and calm",
    "the sacred rhythm of becoming",
    "truth over noise",
    "kindness, courage, and peace",
    "the quiet strength within me"
]

mantra_ends = [
    "because I was always meant for this.",
    "as a warrior of light.",
    "in reverence to who I am becoming.",
    "with trust, not tension."
]

def generate_mantra():
    return f"{random.choice(mantra_starts)} {random.choice(mantra_themes)} {random.choice(mantra_ends)}"

# Generate a daily prompt
def generate_prompt():
    return {
        "date": datetime.today().strftime('%Y-%m-%d'),
        "morning_intention": random.choice(morning_intentions),
        "mantra": generate_mantra(),
        "aligned_action": random.choice(aligned_actions),
        "evening_reflection": random.choice(evening_reflections)
    }

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
st.markdown(f"**🌙 Evening Reflection:** {prompt['evening_reflection']}")

# Journaling Section
st.markdown("---")
st.subheader("📓 Reflection Journal")

journal_entry = st.text_area("Write your thoughts, intentions, or reflections here:")

if st.button("Save Reflection"):
    if journal_entry.strip():
        with open("reflections.txt", "a") as file:
            file.write(f"\n[{prompt['date']}]\n{journal_entry}\n")
        st.success("Reflection saved.")
    else:
        st.warning("Please write something before saving.")

# Regenerate Prompt
st.markdown("---")
if st.button("🔁 Regenerate Today's Prompt"):
    st.experimental_rerun()
