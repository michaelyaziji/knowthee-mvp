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

<<<<<<< HEAD
/* Header bar */
=======
>>>>>>> a827ede (WIP: local changes before rebase)
.header-bar {
    background-color: #0a2c4d;
    padding: 2.5rem 2rem 2rem 2rem;
    color: white;
    border-radius: 0 0 24px 24px;
    margin-bottom: 2rem;
}

.header-title {
<<<<<<< HEAD
    font-size: 2.5rem;
=======
    font-size: 2.7rem;
>>>>>>> a827ede (WIP: local changes before rebase)
    font-weight: 700;
    color: white;
    margin-bottom: 0.5rem;
}

.header-subtitle {
<<<<<<< HEAD
    font-size: 2rem;
=======
    font-size: 1.35rem;
>>>>>>> a827ede (WIP: local changes before rebase)
    font-weight: 400;
    color: #e0e6ed;
    margin-bottom: 0.5rem;
}

<<<<<<< HEAD
=======
.progress-cue {
    font-size: 1.15rem;
    color: #0a2c4d;
    margin-bottom: 2.2rem;
    font-weight: 500;
}

>>>>>>> a827ede (WIP: local changes before rebase)
.section-title {
    color: #0a2c4d;
    font-size: 2rem;
    font-weight: 700;
    margin-top: 2.5rem;
    margin-bottom: 1rem;
}

<<<<<<< HEAD
=======
.section-desc {
    color: #333;
    font-size: 1.1rem;
    margin-bottom: 0.7rem;
    margin-top: -0.5rem;
}

>>>>>>> a827ede (WIP: local changes before rebase)
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

<<<<<<< HEAD
=======
.bold-action {
    font-weight: 700;
    color: #0a2c4d;
}

.key-idea {
    color: #ffc72c;
    font-weight: 700;
}

.stCaption, .stMarkdown, .stTextInput, .stTextArea, .stFileUploader {
    font-size: 1.05rem !important;
}

>>>>>>> a827ede (WIP: local changes before rebase)
/* Hide Streamlit default header and footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""

# Load environment variables
load_dotenv()

# Initialize session state
<<<<<<< HEAD
if 'processed_docs' not in st.session_state:
    st.session_state.processed_docs = []
=======
if 'subject_docs' not in st.session_state:
    st.session_state.subject_docs = []
if 'context_docs' not in st.session_state:
    st.session_state.context_docs = []
if 'team_docs' not in st.session_state:
    st.session_state.team_docs = []
>>>>>>> a827ede (WIP: local changes before rebase)
if 'profile' not in st.session_state:
    st.session_state.profile = None
if 'user_question' not in st.session_state:
    st.session_state.user_question = ''
if 'question_answer' not in st.session_state:
    st.session_state.question_answer = None
if 'reference_docs' not in st.session_state:
    st.session_state.reference_docs = []
<<<<<<< HEAD
=======
if 'intent' not in st.session_state:
    st.session_state.intent = "Coach for promotion"
if 'intent_other' not in st.session_state:
    st.session_state.intent_other = ''
>>>>>>> a827ede (WIP: local changes before rebase)

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
<<<<<<< HEAD
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
=======
    st.markdown(
        '<div class="header-bar">'
        '<div class="header-title">Leadership Profile</div>'
        '<div class="header-subtitle">Upload relevant documents to generate customized insights.</div>'
        '</div>',
        unsafe_allow_html=True
    )
    st.markdown("<div class=\"progress-cue\">We'll generate a <span class=\"key-idea\">custom leadership profile</span> and tailored guidance based on what you share. By default we will generate: <br> 1. An integrated leadership profile <br> 2. Key Strengths <br> 3. Potential Derailers <br> 4. Overall Leadership Style <br> 5. A chart indicating what types of jobs would be most and least suitable for this person, and why</div>", unsafe_allow_html=True)

    # What do you need? (Intent) Dropdown
    intent_options = [
        "Get an oveall assessment",
        "Coach for promotion",
        "Evaluate role fit",
        "Build onboarding plan",
        "Guide a development plan",
        "Other (please specify)"
    ]
    st.markdown('<div style="margin-bottom: 1.2rem;"><span class="bold-action">What outcome are you seeking?</span></div>', unsafe_allow_html=True)
    intent = st.selectbox(" ", intent_options, key="intent")
    intent_other = ""
    if intent == "Other (please specify)":
        intent_other = st.text_input("Please specify your outcome or use case:", key="intent_other")

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)  # Extra spacing

    # Leadership Subject Documents
    st.markdown('<div class="section-title"> Documents about the Individual <span style="font-size:1.2rem; font-weight:400;"> </span></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">Help us get to know this leader. The more you share, the more useful the profile will be. <span class="bold-action">Upload</span> assessments, CVs, 360s, and other insights that reveal how they think, act, and lead.</div>', unsafe_allow_html=True)
    subject_docs = st.file_uploader(
        "Upload PDF or DOCX", type=['pdf', 'docx'], accept_multiple_files=True, key="subject"
    )

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # Context Documents
    st.markdown('<div class="section-title">Context Documents <span style="font-size:1.2rem; font-weight:400;">(What\'s the leadership context?)</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-desc">What would he helpful for us to know? <span class="bold-action">Upload</span> role descriptions, leadership models, or team member profiles to help us align the profile to future needs.</div>', unsafe_allow_html=True)
    context_docs = st.file_uploader(
        "Upload PDF or DOCX", type=['pdf', 'docx'], accept_multiple_files=True, key="context"
    )

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # Prompt box with examples
    st.markdown(
        '<div style="color: #888; font-size: 1.05em; margin-top:1.5rem;">'
        'Do you have any specific questions in mind? <br>'
        'Examples: "Is this leader a good fit for the regional GM role?" • '
        '"How can we accelerate their readiness for executive committee?" • '
        '"What coaching areas should we prioritize?"'
        '</div>', unsafe_allow_html=True
    )
    user_question = st.text_area(" ", height=80, key="user_question")

    if st.button("Submit"):
        st.session_state.subject_docs = []
        st.session_state.context_docs = []
        st.session_state.question_answer = None
        st.session_state.profile = None
        all_docs = list(st.session_state.reference_docs)
        with st.spinner("Processing documents..."):
            # Process subject docs
            if subject_docs:
                for file in subject_docs:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.name)[1]) as tmp_file:
                        tmp_file.write(file.getvalue())
                        processed_text = document_processor.process_document(tmp_file.name)
                        st.session_state.subject_docs.append(processed_text)
                        os.unlink(tmp_file.name)
                all_docs.extend(st.session_state.subject_docs)
            # Process context docs
            if context_docs:
                for file in context_docs:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.name)[1]) as tmp_file:
                        tmp_file.write(file.getvalue())
                        processed_text = document_processor.process_document(tmp_file.name)
                        st.session_state.context_docs.append(processed_text)
                        os.unlink(tmp_file.name)
                all_docs.extend(st.session_state.context_docs)
>>>>>>> a827ede (WIP: local changes before rebase)
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