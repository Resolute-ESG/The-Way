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
            model="gpt-4",
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
        st.warning("New Soul Guides have been generated to support your Journey.")
