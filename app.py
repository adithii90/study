import streamlit as st
from PyPDF2 import PdfReader
from transformers import pipeline
import textwrap
import random

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Study Notes Generator",
    page_icon="📚",
    layout="wide"
)

# -----------------------------
# LOAD AI SUMMARIZER
# -----------------------------
@st.cache_resource
def load_summarizer():
    return pipeline(
        "summarization",
        model="facebook/bart-large-cnn"
    )

summarizer = load_summarizer()

# -----------------------------
# FUNCTIONS
# -----------------------------

# Extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""

    pdf_reader = PdfReader(pdf_file)

    for page in pdf_reader.pages:
        text += page.extract_text()

    return text


# Generate summary
def generate_summary(text):

    text = text[:3000]

    summary = summarizer(
        text,
        max_length=200,
        min_length=50,
        do_sample=False
    )

    return summary[0]['summary_text']


# Generate quiz questions
def generate_quiz(text):

    sentences = text.split('.')

    quiz = []

    for i in range(min(5, len(sentences))):

        sentence = sentences[i].strip()

        if len(sentence) > 20:

            words = sentence.split()

            if len(words) > 5:

                answer = random.choice(words)

                question = sentence.replace(
                    answer,
                    "_______"
                )

                quiz.append({
                    "question": question,
                    "answer": answer
                })

    return quiz


# Generate flashcards
def generate_flashcards(text):

    sentences = text.split('.')

    flashcards = []

    for sentence in sentences[:10]:

        sentence = sentence.strip()

        if len(sentence) > 30:

            parts = sentence.split()

            title = " ".join(parts[:4])

            flashcards.append({
                "question": title + "...?",
                "answer": sentence
            })

    return flashcards


# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("📘 AI Study Notes")

option = st.sidebar.radio(
    "Choose Input Type",
    ["Upload PDF", "Paste Text"]
)

# -----------------------------
# MAIN TITLE
# -----------------------------
st.title("📚 AI Study Notes Generator")

st.markdown("""
Generate:
- ✨ Smart Summaries
- 📝 Quiz Questions
- 🎴 Flashcards

using Artificial Intelligence.
""")

# -----------------------------
# INPUT SECTION
# -----------------------------
text = ""

if option == "Upload PDF":

    uploaded_file = st.file_uploader(
        "Upload your PDF",
        type=["pdf"]
    )

    if uploaded_file is not None:

        with st.spinner("Extracting text from PDF..."):
            text = extract_text_from_pdf(uploaded_file)

        st.success("PDF uploaded successfully!")

elif option == "Paste Text":

    text = st.text_area(
        "Paste your study material here",
        height=300
    )

# -----------------------------
# PROCESS BUTTONS
# -----------------------------
if text:

    st.subheader("📄 Preview")

    st.write(text[:1000] + "...")

    col1, col2, col3 = st.columns(3)

    # -----------------------------
    # SUMMARY
    # -----------------------------
    with col1:

        if st.button("✨ Generate Notes"):

            with st.spinner("Generating summary..."):

                summary = generate_summary(text)

            st.subheader("📌 Summary Notes")

            st.success(summary)

    # -----------------------------
    # QUIZ
    # -----------------------------
    with col2:

        if st.button("📝 Generate Quiz"):

            quiz = generate_quiz(text)

            st.subheader("🧠 Quiz Questions")

            for idx, q in enumerate(quiz):

                st.markdown(f"""
                ### Q{idx+1}
                {q['question']}

                ✅ Answer: **{q['answer']}**
                """)

    # -----------------------------
    # FLASHCARDS
    # -----------------------------
    with col3:

        if st.button("🎴 Generate Flashcards"):

            flashcards = generate_flashcards(text)

            st.subheader("📚 Flashcards")

            for idx, card in enumerate(flashcards):

                with st.expander(f"Flashcard {idx+1}"):

                    st.markdown(f"""
                    **Question:**  
                    {card['question']}

                    **Answer:**  
                    {card['answer']}
                    """)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")

st.caption("Made with ❤️ using Streamlit + AI")
