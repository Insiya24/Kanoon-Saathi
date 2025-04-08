# legal_research.py

import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# Configure Gemini API key
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key = api_key)

# Load models
text_model = genai.GenerativeModel('gemini-1.5-pro')
vision_model = genai.GenerativeModel('gemini-1.5-pro')

# Define the app function
def legal_research_app():
    st.title("⚖ AI Legal Research Assistant")
    st.markdown("Welcome to your AI-powered legal research assistant. Select your task from the dropdown below.")

    if "legal_output" not in st.session_state:
        st.session_state.legal_output = ""
    if "translated_output" not in st.session_state:
        st.session_state.translated_output = ""

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        goal = st.selectbox(
            "🎯 Select Your Research Goal",
            [
                "AI Legal Summarizer",
                "Summarize a Case",
                "Generate Legal Draft",
                "Check Legal Validity",
                "Compare Two Laws",
                "Suggest Related Cases",
                "Explain Legal Terms"
            ]
        )

        if goal == "AI Legal Summarizer":
            uploaded_pdf = st.file_uploader("📄 Upload a Legal PDF", type=["pdf"])

            if uploaded_pdf:
                if st.button("🧠 Generate Summary"):
                    with st.spinner("Summarizing the legal PDF..."):
                        try:
                            pdf_reader = PdfReader(uploaded_pdf)
                            pdf_text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
                            response = vision_model.generate_content(["Summarize this legal PDF:", pdf_text])
                            st.session_state.legal_output = response.text
                            st.success("✅ Summary Generated")
                            st.markdown(response.text)
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")

            if st.session_state.legal_output:
                lang = st.selectbox("🌐 Translate Summary to:", ["", "Hindi", "Telugu", "Tamil", "French", "German"])
                if lang:
                    with st.spinner(f"Translating to {lang}..."):
                        try:
                            translation_prompt = f"Translate this to {lang}:\n\n{st.session_state.legal_output}"
                            translation_response = text_model.generate_content(translation_prompt)
                            st.session_state.translated_output = translation_response.text
                            st.success(f"🌐 Translated to {lang}")
                            st.markdown(translation_response.text)
                        except Exception as e:
                            st.error(f"❌ Translation Error: {str(e)}")

        else:
            query = st.text_area("📝 Enter Your Legal Query", height=150)
            context = st.text_input("📎 Optional Legal Context")

            def build_prompt(goal, query, context):
                base_context = f"\n\nAdditional Context: {context if context else 'None'}"

                if goal == "Summarize a Case":
                    return f"""
                    You are a legal research assistant specializing in Indian law.
                    Summarize the following case. Include background, legal issues, arguments, judgment, and its significance.
                    Query: {query}{base_context}
                    Keep the tone professional and suitable for lawyers and students.
                    """

                elif goal == "Generate Legal Draft":
                    return f"""
                    You are an expert legal drafter.
                    Generate a formal legal draft based on the following input. Use proper structure and legal formatting.
                    Request: {query}{base_context}
                    Ensure legal soundness and clarity.
                    """

                elif goal == "Check Legal Validity":
                    return f"""
                    You are a legal analyst well-versed in Indian law.
                    Check if the following issue or clause is legally valid. Support your answer with relevant Indian laws and past judgments.
                    Issue: {query}{base_context}
                    Provide a clear and legally sound opinion.
                    """

                elif goal == "Compare Two Laws":
                    return f"""
                    You are a comparative legal researcher.
                    Compare the following laws, clauses, or sections. Explain their differences, similarities, and legal implications.
                    Comparison: {query}{base_context}
                    Present the information in a professional and structured manner.
                    """

                elif goal == "Suggest Related Cases":
                    return f"""
                    You are a legal researcher.
                    Suggest related Indian legal cases relevant to the following topic. Provide case summaries and citations.
                    Topic: {query}{base_context}
                    Present 3–5 top cases with legal relevance.
                    """

                elif goal == "Explain Legal Terms":
                    return f"""
                    You are a legal glossary expert.
                    Explain the meaning of the following legal term in simple language. Include origin, examples, and context in Indian law.
                    Term: {query}{base_context}
                    Make it clear and suitable for students.
                    """

            if st.button("🔎 Generate Response"):
                if not query:
                    st.warning("🚨 Please enter a legal query.")
                else:
                    with st.spinner("Generating legal response..."):
                        try:
                            prompt = build_prompt(goal, query, context)
                            response = text_model.generate_content(prompt)
                            st.session_state.legal_output = response.text
                            st.success("✅ Response Generated")
                            st.markdown(response.text)
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")

    st.markdown("---")
    st.caption("📌 *Disclaimer:* This tool is for educational and research purposes only. It does not constitute legal advice.")
