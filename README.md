# Gemini Scholar

A smart flashcard generator that helps you make study notes and flashcards from PDFs using AI. Born from the frustration of switching between PDFs and notes during exams.

## Features

- Upload a PDF and get summarized notes
- Auto-generate flashcards
- AI-powered using Gemini API

## Tech Stack

- Python
- Streamlit
- Google Generative AI
- pdfplumber, PyMuPDF
- BeautifulSoup4, requests
- groq (optional)

## Setup

```bash
# Clone the repo
git clone https://github.com/your-username/gemini-scholar.git
cd gemini-scholar

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Set your API keys
touch .env
# Add GOOGLE_API_KEY and GROQ_API_KEY inside .env

# Run the app
streamlit run app.py
