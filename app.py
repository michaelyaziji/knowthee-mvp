import streamlit as st
import os
from dotenv import load_dotenv
import tempfile
from document_processor import DocumentProcessor
from profile_generator import ProfileGenerator
from vector_store import VectorStore
from fpdf import FPDF

# Custom CSS for branding and layout
CUSTOM_CSS = """
<style>
body {
    background-color: #f8f9fa;
}

/* Header bar */
.header-bar {
    background-color: #0a2c4d;
    padding: 2.5rem 2rem 2rem 2rem;
    color: white;
    border-radius: 0 0 24px 24px;
    margin-bottom: 2rem;
}

.header-title {
    font-size: 2.5rem;
    font-weight: 700;
    color: white;
    margin-bottom: 0.5rem;
}

.header-subtitle {
    font-size: 2rem;
    font-weight: 400;
    color: #e0e6ed;
    margin-bottom: 0.5rem;
}

.section-title {
    color: #0a2c4d;
    font-size: 2rem;
    font-weight: 700;
    margin-top: 2.5rem;
    margin-bottom: 1rem;
}

.profile-section {
    background: white;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    box-shadow: 0 2px 8px rgba(10,44,77,0.07);
}

.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100vw;
    background: #0a2c4d;
    color: #ffc72c;
    text-align: right;
    font-size: 3rem;
    font-weight: 900;
    padding: 0.7rem 2.5rem;
    letter-spacing: 2.5px;
    z-index: 100;
}

/* Hide Streamlit default header and footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""

# Load environment variables
load_dotenv()

# Initialize session state
if 'processed_docs' not in st.session_state:
    st.session_state.processed_docs = []
if 'profile' not in st.session_state:
    st.session_state.profile = None
if 'user_question' not in st.session_state:
    st.session_state.user_question = ''
if 'question_answer' not in st.session_state:
    st.session_state.question_answer = None
if 'reference_docs' not in st.session_state:
    st.session_state.reference_docs = []

# Initialize components
document_processor = DocumentProcessor()
vector_store = VectorStore()
profile_generator = ProfileGenerator()

# Load and process reference PDFs from HowToInterpretHogans/
def load_reference_docs():
    reference_folder = "HowToInterpretHogans"
    reference_texts = []
    for filename in os.listdir(reference_folder):
        if filename.lower().endswith('.pdf'):
            file_path = os.path.join(reference_folder, filename)
            try:
                text = document_processor.process_document(file_path)
                reference_texts.append(text)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
    return reference_texts

# Only load reference docs once per session
if not st.session_state.reference_docs:
    st.session_state.reference_docs = load_reference_docs()

def create_pdf(profile_text, question_answer=None):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, profile_text)
    if question_answer:
        pdf.ln(10)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Special Question Answer:", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, question_answer)
    return pdf.output(dest='S').encode('latin1')

def main():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    # Custom header bar
    st.markdown(
        '<div class="header-bar">'
        '<div class="header-title">Comprehensive Integrated Leadership Profile</div>'
        '<div class="header-subtitle">Upload leadership documents to generate a customized profile</div>'
        '</div>',
        unsafe_allow_html=True
    )
    
    # File upload section
    with st.container():
        st.markdown('<div style="font-size:1.8rem; font-weight:400; margin-bottom:0.5rem;">Upload leadership documents (Hogan Report, CV, 360, Big Five, etc.)(in PDF)</div>', unsafe_allow_html=True)
        uploaded_files = st.file_uploader(
            " ",  # Hide the default label
            type=['pdf', 'docx'],
            accept_multiple_files=True,
            key="file_uploader"
        )

    # User question input
    st.markdown('<div style="font-size:1.8rem; font-weight:400; margin-top:1.5rem; margin-bottom:0.5rem;">Do you have any special questions about this leader? For example, fitness for a role, or team? Or how best to coach them for a specific next job? (Optional)</div>', unsafe_allow_html=True)
    user_question = st.text_input(
        " ",  # Hide the default label
        value=st.session_state.user_question
    )

    # Submit button
    if st.button("Submit"):
        st.session_state.processed_docs = []
        st.session_state.user_question = user_question
        st.session_state.question_answer = None
        st.session_state.profile = None
        # Always include reference docs
        all_docs = list(st.session_state.reference_docs)
        if uploaded_files:
            with st.spinner("Processing documents..."):
                for file in uploaded_files:
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.name)[1]) as tmp_file:
                        tmp_file.write(file.getvalue())
                        processed_text = document_processor.process_document(tmp_file.name)
                        st.session_state.processed_docs.append(processed_text)
                        os.unlink(tmp_file.name)
                all_docs.extend(st.session_state.processed_docs)
        else:
            with st.spinner("Loading reference documents..."):
                pass  # Just use reference docs
        # Store all documents in vector database
        vector_store.store_documents(all_docs)
        # Generate profile
        st.session_state.profile = profile_generator.generate_profile(
            vector_store.get_relevant_chunks()
        )
        # If user provided a question, get an answer and append it
        if user_question.strip():
            st.session_state.question_answer = profile_generator.answer_question(
                vector_store.get_relevant_chunks(), user_question
            )

    # Display profile if available
    if st.session_state.profile:
        st.markdown('<div class="section-title">Executive Summary</div>', unsafe_allow_html=True)
        st.markdown('<div class="profile-section">', unsafe_allow_html=True)
        st.write(st.session_state.profile)
        st.markdown('</div>', unsafe_allow_html=True)
        # Display answer to user question if provided
        if st.session_state.question_answer:
            st.markdown('<div class="section-title">Special Question Answer</div>', unsafe_allow_html=True)
            st.markdown('<div class="profile-section">', unsafe_allow_html=True)
            st.write(st.session_state.question_answer)
            st.markdown('</div>', unsafe_allow_html=True)
        # Export to PDF download button
        pdf_bytes = create_pdf(st.session_state.profile, st.session_state.question_answer)
        st.download_button(
            label="Export to PDF",
            data=pdf_bytes,
            file_name="leadership_profile.pdf",
            mime="application/pdf"
        )

    # Custom footer
    st.markdown('<div class="footer">KNOWTHEE.AI</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main() 