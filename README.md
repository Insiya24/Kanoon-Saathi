# ⚖️ Kanoon Saathi – AI-Powered Legal Assistant

India’s legal system faces massive challenges: over 5.3 crore pending cases and millions unaware of their legal rights. **Kanoon Saathi** is a tech-driven lawtech solution that empowers citizens, speeds up legal processes, and increases transparency using AI.

## 🚀 Key Features

### 1. 📚 Citizen & Law
- Region-specific legal education platform
- Covers criminal law, consumer rights, cyber laws & women’s protection
- Multilingual support
- Helps users file FIRs, RTIs, and understand basic rights

### 2. 🔓 Bail Reckoner
- AI tool for evaluating bail eligibility
- Uses crime details, jail time & court guidelines
- Designed for jail staff, legal aid workers & judges
- Supports integration with platforms like ePrisons

### 3. 🧠 AI Legal Research Engine
- Accelerates legal research for commercial courts
- Analyzes past judgments & laws using AI
- Supports regional languages
- Reduces legal research time by over 50%

### 4. 🗳️ Case Prioritization System
- Public voting system for legal cases
- Accepts anonymous testimonials and evidence
- Creates a priority list based on public concern

## 📁 Project Structure

ExploreFeaturesApp/ 
│ 
├── features/ 
│ ├── case_prioritization.py 
│ ├── legal_research.py 
│ ├── bail_reckoner.py 
│ └── citizen_law.py 
│ 
├── uploads/ 
# Proofs uploaded for testimonials 
├── cases.csv 
├── upvotes.csv 
├── testimonials.csv 
├── main_app.py # Streamlit app entry point 
├── requirements.txt 
└── .streamlit/ 
└── CONFIG.toml 

---

---

## ▶️ How to Run Locally

1. **Clone the repo:**
git clone https://github.com/your-username/legal-ai-system.git
cd legal-ai-system

2. **Install requirements:**
pip install -r requirements.txt
Add Gemini API Key:
Create a file: .streamlit/secrets.toml
[gemini]
api_key = "your_actual_gemini_key_here"

3. **Run the app:**
streamlit run main_app.py



> 💡 *Kanoon Saathi* brings law closer to the people—accessible, understandable, and participatory.
