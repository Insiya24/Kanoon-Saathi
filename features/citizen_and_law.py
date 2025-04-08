# features/citizen_law.py
import streamlit as st
import google.generativeai as genai
import json
from datetime import datetime

api_key = st.secrets["GEMINI_API_KEY_1"]
genai.configure(api_key)
model = genai.GenerativeModel("gemini-1.5-pro")

LEGAL_CATEGORIES = [
    "Criminal and Civil Laws", "Consumer Rights", "Cyber Law Awareness",
    "Laws Protecting Women, Children, and Minorities", "Environmental and Labour Laws"
]

def classify_issue(description):
    prompt = f"""Classify the legal issue below into ONE category from: {LEGAL_CATEGORIES}.
    Issue: "{description}"
    Return only the most appropriate category.
    """
    return model.generate_content(prompt).text.strip()

def generate_summary(convo, category, is_underage):
    note = "Include that the user is underage and should consult legal aid." if is_underage else ""
    prompt = f"""Summarize the conversation under {category} law.
Conversation:
{convo}
Provide:
1. Summary  
2. Applicable Laws  
3. Next Steps
{note}
"""
    return model.generate_content(prompt).text.strip()

def save_case_to_file(name, age, category, chat_history, summary):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"case_{name}_{timestamp}.json"
    case_data = {
        "name": name, "age": age, "category": category,
        "timestamp": timestamp, "chat_history": chat_history, "summary": summary
    }
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(case_data, f, indent=2)
    return file_name

def citizen_law_basic():
    st.subheader("🧑‍⚖ Citizen & Law Assistant")
    with st.form("basic_info"):
        name = st.text_input("Your Name")
        age = st.number_input("Your Age", min_value=1, step=1)
        issue = st.text_input("Describe your legal issue")

        if st.form_submit_button("Start Chat") and name and issue:
            st.session_state.citizen_name = name
            st.session_state.citizen_age = age
            st.session_state.legal_issue = issue
            st.session_state.is_adult = age >= 18
            st.session_state.legal_category = classify_issue(issue)
            st.session_state.citizen_chat_history = [{"role": "user", "parts": [f"My legal issue is: {issue}"]}]
            st.session_state.chat_started = True
            st.session_state.full_chat_mode = True
            st.rerun()

def citizen_law_full_chat():
    st.title("🧑‍⚖ Full Legal Chat Assistant")

    if "awaiting_response" not in st.session_state:
        st.session_state.awaiting_response = False
    if "final_summary_generated" not in st.session_state:
        st.session_state.final_summary_generated = False

    st.success(f"✅ Your issue falls under: {st.session_state.legal_category}")

    for chat in st.session_state.citizen_chat_history:
        with st.chat_message(chat["role"]):
            st.write(chat["parts"][0])

    if st.session_state.awaiting_response:
        with st.spinner("AI thinking..."):
            convo = "\n".join([f"{c['role'].capitalize()}: {c['parts'][0]}" for c in st.session_state.citizen_chat_history])
            prompt = f"""You are a legal assistant. Issue: "{st.session_state.legal_issue}".
Ask questions until enough info. If enough info, say: 'I now have enough information.'

Conversation:
{convo}
"""
            response = model.generate_content(prompt).text.strip()
            if "i now have enough information" in response.lower():
                st.session_state.final_summary_generated = True
                st.session_state.awaiting_response = False
            else:
                st.session_state.citizen_chat_history.append({"role": "assistant", "parts": [response]})
                st.session_state.awaiting_response = False
            st.rerun()

    user_msg = st.chat_input("Your reply:")
    if user_msg:
        st.session_state.citizen_chat_history.append({"role": "user", "parts": [user_msg]})
        if not st.session_state.final_summary_generated:
            st.session_state.awaiting_response = True
            st.rerun()

    if st.session_state.final_summary_generated:
        with st.spinner("Generating summary..."):
            convo = "\n".join([f"{c['role'].capitalize()}: {c['parts'][0]}" for c in st.session_state.citizen_chat_history])
            summary = generate_summary(convo, st.session_state.legal_category, not st.session_state.is_adult)
            st.subheader("📋 Summary & Advice")
            st.write(summary)
            save_case_to_file(
                st.session_state.citizen_name,
                st.session_state.citizen_age,
                st.session_state.legal_category,
                st.session_state.citizen_chat_history,
                summary
            )
        if st.button("🔙 Back to Features"):
            st.session_state.full_chat_mode = False
            st.rerun()
