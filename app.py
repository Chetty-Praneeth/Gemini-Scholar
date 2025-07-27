import streamlit as st
from gemini_utils import generate_summary, generate_flashcards, chat_with_text

st.set_page_config(page_title="Gemini Scholar", page_icon="", layout="wide")

# ---------- CSS for styling ----------
st.markdown("""
    <style>
        .main {
            background-color: #1c1e21;
        }
        .block-container {
            padding-top: 2rem;
        }
        .stTextArea textarea {
            font-size: 1.1rem;
            background-color: #2c2f33;
            color: #f1f1f1;
        }
        .stButton > button {
            background-color: #000000;
            color: white;
            border-radius: 8px;
            padding: 10px 24px;
            font-size: 16px;
            border: 2px solid black;
            transition: all 0.3s ease;
            box-shadow: none;
        }
        .stButton > button:hover {
            background-color: #ffffff;
            color: #000000;
            border: 2px solid black;
            box-shadow: 0 0 0 2px black;
        }
        .title-style {
            font-size: 40px;
            font-weight: 800;
            color: #ffffff;
        }
        .subtitle {
            font-size: 20px;
            color: #cccccc;
        }
        .output-box {
            background-color: #2c2f33;
            padding: 1rem;
            border-radius: 10px;
            color: white;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
    </style>
""", unsafe_allow_html=True)
# InvalidCharacterError
import html
import re
def clean_output(text: str) -> str:
    # Remove control characters
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
    # Escape HTML
    text = html.escape(text)
    # Preserve newlines
    return text.replace('\n', '<br>')


# ---------- Title & Description ----------
st.markdown('<div class="title-style">Gemini Scholar</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload any PDF and instantly get summaries, flashcards, and an AI you can chat with. Research made effortless.</div>', unsafe_allow_html=True)
st.markdown("---")

# ---------- Upload & Input ----------
st.sidebar.header("Upload Document")
uploaded_file = st.sidebar.file_uploader("Choose a .txt or .pdf file", type=["txt", "pdf"])
text_input = st.text_area("Or paste your document text here", height=250)

# ---------- Load Text ----------
text = ""
if uploaded_file:
    if uploaded_file.name.endswith(".txt"):
        text = uploaded_file.read().decode("utf-8")
    elif uploaded_file.name.endswith(".pdf"):
        import fitz
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = "\n".join([page.get_text() for page in doc])
elif text_input:
    text = text_input

# ---------- Session Storage ----------
if "summary" not in st.session_state:
    st.session_state.summary = None
if "flashcards" not in st.session_state:
    st.session_state.flashcards = None
if "answer" not in st.session_state:
    st.session_state.answer = None

# ---------- Actions ----------
if text:
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Generate Summary"):
            with st.spinner("Generating summary..."):
                try:
                    st.session_state.summary = generate_summary(text)
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    with col2:
        if st.button("Generate Flashcards"):
            with st.spinner("Generating flashcards..."):
                try:
                    st.session_state.flashcards = generate_flashcards(text)
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    with col3:
        question = st.text_input("Ask a question from this document", key="qa_input")
        if st.button("Ask"):
            if question.strip():
                with st.spinner("Finding answer..."):
                    try:
                        st.session_state.answer = chat_with_text(text, question)
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

    # ---------- Output Layer ----------
    if st.session_state.summary:
        st.subheader("Summary")
        cleaned = clean_output(st.session_state.summary)
        st.markdown(f'<div class="output-box">{cleaned}</div>', unsafe_allow_html=True)

    if st.session_state.flashcards:
        st.subheader("Flashcards")
        cleaned = clean_output(st.session_state.flashcards)
        st.markdown(f'<div class="output-box">{cleaned}</div>', unsafe_allow_html=True)

    if st.session_state.answer:
        st.subheader("Answer")
        cleaned = clean_output(st.session_state.answer)
        st.markdown(f'<div class="output-box"><b>{cleaned}</b></div>', unsafe_allow_html=True)


else:
    st.info("Upload a file or paste your text to get started.")
