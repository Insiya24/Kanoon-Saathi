# bail_reckoner.py

import streamlit as st
from datetime import datetime
import pdfplumber
import google.generativeai as genai

# Configure Gemini API
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key)

# Create the model
generation_config = {
    "temperature": 0.4,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="learnlm-1.5-pro-experimental",
    generation_config=generation_config,
)

chat_session = model.start_chat(history=[])

# Utility Function: PDF Text Extraction
def get_text_from_any_pdf(pdf_bytes):
    final_text = ""
    with pdfplumber.open(pdf_bytes) as pdf:
        for page in pdf.pages:
            final_text += page.extract_text() or ""
            final_text += "\n"
    return final_text.strip()

# Main app function
def bail_reckoner_app():
    st.title("🔍 Bail Reckoner - Legal Bail Eligibility and Assessment Tool")
    st.markdown("Use this tool to analyze bail eligibility based on legal case inputs.")

    st.header("⿡ Basic Case Information")
    name = st.text_input("Full Name of Accused")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    age = st.number_input("Age", min_value=0, step=1)
    case_number = st.text_input("Case Number / FIR Number")
    court_name = st.text_input("Court Name")
    arrest_date = st.date_input("Date of Arrest")
    offense_desc = st.text_area("Describe the Offense (Charges & Sections)")

    st.header("⿢ Upload Legal Documents (Charge Sheet / FIR / Court Orders)")
    uploaded_docs = st.file_uploader("Upload Legal Documents", type=["pdf"], accept_multiple_files=True)
    collected_text = ""
    for file in uploaded_docs:
        collected_text += get_text_from_any_pdf(file) + "\n\n"

    st.header("⿣ Case Details for Bail Evaluation")
    col1, col2 = st.columns(2)
    with col1:
        is_repeat_offender = st.selectbox("Is Accused a Repeat Offender?", ["No", "Yes"])
        is_offense_bailable = st.selectbox("Is the Offense Bailable?", ["Yes", "No", "Not Sure"])
        has_served_half_term = st.selectbox("Has the accused served at least half the sentence duration (if convicted)?", ["Yes", "No", "Not Applicable"])
    with col2:
        has_cooperation = st.selectbox("Has the Accused Cooperated with Police Investigation?", ["Yes", "No"])
        risk_of_escape = st.selectbox("Is There Any Risk of Escape or Tampering Evidence?", ["No", "Yes", "Unknown"])
        surety_available = st.selectbox("Are Sureties/Personal Bonds Available?", ["Yes", "No"])

    st.header("⿤ Judicial Observations & Remarks (if any)")
    judicial_remarks = st.text_area("Enter Any Relevant Judicial Remarks")

    st.header("⿥ Apply Bail Reckoner Intelligence")
    if st.button("⚖ Analyze Bail Eligibility"):
        with st.spinner("Processing Legal Analysis..."):
            full_prompt = f"""
You are an AI-powered Bail Reckoner assisting judicial authorities, legal aid providers, and undertrial prisoners in determining bail eligibility.

Act like an experienced Indian Judge familiar with IPC, Bhartiya Nyaya Sanhita 2023, Bhartiya Suraksha Sanhita 2023, and Bhartiya Saakshya Adhiniyam 2023. Also consider relevant sections from special statutes (Cyber, SC/ST, Women, Children, State Offenses, Economic, Foreigners).

Use the following inputs to assess the situation:

- Name: {name}
- Gender: {gender}, Age: {age}
- Case No: {case_number}, Court: {court_name}
- Date of Arrest: {arrest_date}
- Offense Description: {offense_desc}
- Repeat Offender: {is_repeat_offender}
- Bailable Offense: {is_offense_bailable}
- Served Half Sentence: {has_served_half_term}
- Cooperation with Investigation: {has_cooperation}
- Risk of Escape/Tampering: {risk_of_escape}
- Surety or Bonds Available: {surety_available}
- Judicial Remarks: {judicial_remarks}
- Extracted Legal Text from Case Docs:
{collected_text}

Evaluate based on:

1. Nature of Offense (Bailable or Not, Compoundable, Severity)
2. Duration Served
3. Judicial Discretion (Escape Risk, Witness Tampering, Cooperation)
4. Procedural Requirements (Surety, Bond)
5. Legal Precedents (Half-term served, Recent SC judgments)
6. Recommendation and Rationale

Give a structured analysis on whether bail can be granted, with reference to applicable legal sections and reasoning.
"""
            try:
                response = chat_session.send_message(full_prompt)
                st.subheader("🧾 Bail Recommendation & Legal Opinion")
                st.markdown(response.text.strip())
            except Exception as e:
                st.error(f"❌ Error generating response: {str(e)}")
