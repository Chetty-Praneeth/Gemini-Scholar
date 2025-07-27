import os
from dotenv import load_dotenv
import google.generativeai as genai
from groq import Groq  # pip install groq

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel("gemini-1.5-flash")

# Configure Groq (LLaMA 3)
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Helper: fallback mechanism
def try_gemini(prompt):
    try:
        return gemini_model.generate_content(prompt).text
    except Exception as e:
        print(f"[Gemini failed] {e}")
        return None

def try_groq(prompt):
    try:
        response = groq_client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="llama3-70b-8192",  # Best model available on Groq
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[Groq failed] {e}")
        return "Sorry, both Gemini and Groq failed to respond."

# Core functions
def generate_summary(text):
    prompt = f"Summarize this document:\n{text[:12000]}"
    result = try_gemini(prompt)
    return result if result else try_groq(prompt)

def generate_flashcards(text):
    prompt = f"Generate 5 Q&A flashcards from this document:\n{text[:12000]}"
    result = try_gemini(prompt)
    return result if result else try_groq(prompt)

def chat_with_text(full_text, question):
    prompt = f"You have read this document:\n{full_text[:12000]}\nAnswer the following question strictly using the document:\n{question}"
    result = try_gemini(prompt)
    return result if result else try_groq(prompt)
