import streamlit as st
from hr_agent import HRAgent
from cfo_agent import CFOAgent
import os
import tempfile
from pathlib import Path
import docx
import io
import base64
import PyPDF2
import pdfplumber
from openai import OpenAI

st.set_page_config(page_title="Custom Menu", layout="wide")

# Initialize session state variables
if 'page' not in st.session_state:
    st.session_state['page'] = 'main'

if 'current_agent' not in st.session_state:
    st.session_state.current_agent = 'HR'

if 'hr_agent' not in st.session_state:
    st.session_state.hr_agent = HRAgent()

if 'cfo_agent' not in st.session_state:
    st.session_state.cfo_agent = CFOAgent()

if 'processing' not in st.session_state:
    st.session_state.processing = False

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'input_key' not in st.session_state:
    st.session_state.input_key = 0

if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []

def read_docx(file):
    try:
        doc = docx.Document(file)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)
    except Exception as e:
        return f"Error reading DOCX file: {str(e)}"

def read_text_file(file):
    try:
        # Try different encodings
        encodings = ['utf-8', 'latin-1', 'cp1252']
        for encoding in encodings:
            try:
                return file.read().decode(encoding)
            except UnicodeDecodeError:
                file.seek(0)  # Reset file pointer
                continue
        return "Error: Could not decode file with any supported encoding"
    except Exception as e:
        return f"Error reading text file: {str(e)}"

def read_pdf(file):
    """Read text from a PDF file using multiple methods for better extraction"""
    try:
        # First try with pdfplumber for better text extraction
        with pdfplumber.open(file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
            if text.strip():
                return text

        # Fallback to PyPDF2 if pdfplumber doesn't extract text well
        file.seek(0)  # Reset file pointer
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        return f"Error reading PDF file: {str(e)}"

def save_uploaded_file(uploaded_file):
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
            # Write the uploaded file to the temporary file
            tmp_file.write(uploaded_file.getvalue())
            return tmp_file.name
    except Exception as e:
        st.error(f"Error saving file: {str(e)}")
        return None

def encode_file_to_base64(file_data, file_name):
    """Encode file data to base64 string with appropriate data URI"""
    file_extension = Path(file_name).suffix.lower()
    mime_types = {
        '.pdf': 'application/pdf',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.txt': 'text/plain'
    }
    mime_type = mime_types.get(file_extension, 'application/octet-stream')
    base64_string = base64.b64encode(file_data).decode('utf-8')
    return f"data:{mime_type};base64,{base64_string}"

def process_uploaded_files():
    if st.session_state.uploaded_files:
        file_contents = []
        for uploaded_file in st.session_state.uploaded_files:
            file_extension = Path(uploaded_file.name).suffix.lower()
            file_data = uploaded_file.getvalue()
            
            try:
                if file_extension == '.pdf':
                    # For PDFs, we'll use the responses API
                    base64_string = base64.b64encode(file_data).decode('utf-8')
                    file_contents.append({
                        "type": "file",
                        "file": {
                            "filename": uploaded_file.name,
                            "data": f"data:application/pdf;base64,{base64_string}"
                        }
                    })
                elif file_extension == '.docx':
                    # Handle DOCX files
                    content = read_docx(io.BytesIO(file_data))
                    file_contents.append({
                        "type": "text",
                        "text": f"File: {uploaded_file.name}\nContent:\n{content}"
                    })
                else:
                    # Handle text files
                    content = read_text_file(io.BytesIO(file_data))
                    file_contents.append({
                        "type": "text",
                        "text": f"File: {uploaded_file.name}\nContent:\n{content}"
                    })
            except Exception as e:
                st.error(f"Error processing file {uploaded_file.name}: {str(e)}")
                continue
                
        return file_contents
    return None

def change_agent():
    # Clear chat history when changing agents
    st.session_state.messages = []
    st.session_state.input_key += 1
    if st.session_state.current_agent == 'HR':
        st.session_state.hr_agent.clear_history()
    else:
        st.session_state.cfo_agent.clear_history()

def truncate_message(message, max_length=4000):
    """Truncate a message if it's too long"""
    if len(message) > max_length:
        return message[:max_length] + "..."
    return message

def get_recent_messages(messages, max_messages=15):
    """Get the most recent messages to stay within token limits"""
    recent = messages[-max_messages:] if len(messages) > max_messages else messages
    # Truncate each message to reduce token count
    return [{"role": msg["role"], "content": truncate_message(msg["content"])} for msg in recent]

st.markdown('''
    <style>
    /* Make all Streamlit menu icon buttons and their emoji much larger */
    .stButton > button {
        font-size: 8rem !important;
        height: 180px !important;
        width: 180px !important;
        line-height: 1 !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    .stButton > button span {
        font-size: 8rem !important;
        line-height: 1 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    </style>
''', unsafe_allow_html=True)

# Page navigation using session state
if 'page' not in st.session_state:
    st.session_state['page'] = 'main'

def go_to_brain():
    st.session_state['page'] = 'brain'

def go_to_main():
    st.session_state['page'] = 'main'

menu_col, content_col, separator_col, banner_col = st.columns([1, 3, 0.05, 1])

with menu_col:
    st.markdown('<div class="menu-col">', unsafe_allow_html=True)
    if st.session_state['page'] == 'main':
        if st.button('💬', key='chat_icon', help='Main', use_container_width=True, type='secondary'):
            st.session_state['page'] = 'main'
        if st.button('🧠', key='brain_icon', help='Go to Add Info', use_container_width=True, type='secondary'):
            st.session_state['page'] = 'brain'
    else:
        if st.button('💬', key='chat_icon_back', help='Go to Main', use_container_width=True, type='secondary'):
            st.session_state['page'] = 'main'
        if st.button('🧠', key='brain_icon_back', help='Add Info', use_container_width=True, type='secondary'):
            st.session_state['page'] = 'brain'
    st.markdown('</div>', unsafe_allow_html=True)

if st.session_state['page'] == 'main':
    with content_col:
        st.markdown('<div class="content-col">', unsafe_allow_html=True)
        st.markdown('<div>', unsafe_allow_html=True)
        st.markdown('<div id="repsmate-title">Repcore Assistant</div>', unsafe_allow_html=True)
        
        # Display chat history
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div style="text-align: right; margin: 10px 0;"><div style="background-color: #e6f2fa; padding: 10px; border-radius: 10px; display: inline-block;">{message["content"]}</div></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="text-align: left; margin: 10px 0;"><div style="background-color: #f0f0f0; padding: 10px; border-radius: 10px; display: inline-block;">{message["content"]}</div></div>', unsafe_allow_html=True)
        
        # Add agent selection dropdown
        agent = st.selectbox(
            "Select Assistant",
            ["HR", "CFO"],
            key="agent_selector",
            on_change=change_agent
        )
        st.session_state.current_agent = agent
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat input container
        st.markdown('<div id="bottom-chat-container">', unsafe_allow_html=True)
        st.markdown('<div class="big-label" style="text-align:left;">Type here</div>', unsafe_allow_html=True)
        
        # Chat input with dynamic key
        user_input = st.text_input("Ask me", label_visibility="collapsed", key=f"main_chat_input_{st.session_state.input_key}")
        
        if user_input:
            # Add user message to display
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Process uploaded files if any
            file_contents = process_uploaded_files()
            
            # Prepare the message content
            message_content = []
            
            # Add file contents if any
            if file_contents:
                message_content.extend(file_contents)
            
            # Add the user's text input
            message_content.append({
                "type": "text",
                "text": user_input
            })
            
            # Get response from selected agent using only recent messages
            recent_messages = get_recent_messages(st.session_state.messages)
            if st.session_state.current_agent == 'HR':
                response = st.session_state.hr_agent.get_response(message_content, recent_messages)
            else:
                response = st.session_state.cfo_agent.get_response(message_content, recent_messages)
            
            # Add assistant response to display
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Clear uploaded files after processing
            st.session_state.uploaded_files = []
            
            # Increment input key to clear the input
            st.session_state.input_key += 1
            
            # Rerun to update the display
            st.rerun()
        
        # File upload section
        uploaded_files = st.file_uploader(
            "Upload files",
            accept_multiple_files=True,
            type=['txt', 'docx', 'pdf'],
            key="file_uploader",
            help="Drag and drop files here or click to browse. Supported formats: TXT, DOCX, PDF"
        )
        if uploaded_files:
            st.session_state.uploaded_files = uploaded_files
            st.success(f"Uploaded {len(uploaded_files)} file(s)")
        
        st.markdown('</div>', unsafe_allow_html=True)
else:
    with content_col:
        st.markdown('<div class="content-col">', unsafe_allow_html=True)
        st.markdown('<div>', unsafe_allow_html=True)
        st.markdown('<div id="repsmate-title">Add Info</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div style="margin-top:2rem;">', unsafe_allow_html=True)
        q = st.text_input("Question:", label_visibility="visible")
        a = st.text_input("Answer:", label_visibility="visible")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with separator_col:
    st.markdown('<div class="separator-line"></div>', unsafe_allow_html=True)

with banner_col:
    st.markdown('<div class="banner-col">', unsafe_allow_html=True)
    st.markdown('<div class="banner" style="margin-top:0;">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:3.2rem;font-weight:900;color:#fff;margin-bottom:1.5rem;">Company Vision</div>', unsafe_allow_html=True)
    st.markdown('<div class="banner-text">', unsafe_allow_html=True)
    st.markdown("""
<ul>
<li>nu exista intrebari stupide</li>
<li>comunicare deschisa si constanta</li>
<li>feedback-ul si ideile sunt binevenite</li>
<li>tinem cont de deadline-uri – ne asumam ce promitem si comunicam daca apar obstacole</li>
<li>autonomie cu responsabilitate – aveti libertate, dar si responsabilitatea rezultatului</li>
<li>ne ajutam intre noi, pentru ca suntem o echipa</li>
</ul>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Reminders section
    st.markdown('<div class="reminders-container">', unsafe_allow_html=True)
    st.markdown('<div class="reminders-title">Reminders</div>', unsafe_allow_html=True)
    reminders = st.text_area("Add or edit reminders here...", key="reminders_section", height=600, label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Add CSS for file upload section
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    height: 100vh !important;
    overflow: hidden !important;
}
[data-testid="stAppViewContainer"] > .main {
    height: 100vh !important;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.flex-content-col {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    height: 100%;
    min-height: 0;
}
.big-icon {
    font-size: 80px;
    display: block;
    margin-bottom: 40px;
    margin-top: 10px;
    cursor: pointer;
}
.menu-col {
    min-width: 120px;
    max-width: 180px;
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
    z-index: 100;
}
.menu-col .stButton > button, .stButton > button[data-testid^="chat_icon"], .stButton > button[data-testid^="brain_icon"] {
    font-size: 10.5rem !important;
    height: 330px !important;
    width: 330px !important;
    line-height: 1 !important;
}
.separator-col {
    display: flex;
    align-items: stretch;
    justify-content: center;
    position: fixed;
    left: 180px;
    top: 0;
    bottom: 0;
    z-index: 99;
}
.separator-line {
    width: 2px;
    background: #d3d3d3;
    height: 100vh;
    margin: 0 auto;
    border-radius: 2px;
}
.content-col {
    margin-left: 200px;
    margin-right: 320px;
    height: 100vh;
    overflow-y: auto;
    padding: 20px;
    position: relative;
}
.banner-col {
    position: fixed;
    right: 0;
    top: 0;
    bottom: 0;
    width: 320px;
    z-index: 98;
    padding: 20px;
    display: flex;
    flex-direction: column;
    height: 100vh;
    overflow: hidden;
}
/* Make title bigger */
#repsmate-title {
    font-size: 3.5rem !important;
    font-weight: 900 !important;
    margin-bottom: 1.5rem;
}
/* Make body and label text bigger */
.big-body {
    font-size: 1.5rem !important;
    margin-bottom: 1rem;
}
.big-label {
    font-size: 1.2rem !important;
    font-weight: 700 !important;
    margin-bottom: 0.5rem;
}
/* Make input and output text bigger */
input, .stTextInput > div > input {
    font-size: 1.3rem !important;
}
.stMarkdown p, .stTextInput, .stTextInput label, .stTextInput div {
    font-size: 1.3rem !important;
}
.stButton > button {
    font-size: 80px !important;
    height: 100px !important;
    width: 100px !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    text-align: left !important;
    margin-bottom: 40px !important;
    margin-top: 10px !important;
    padding: 0 !important;
    display: block !important;
}
#bottom-chat-container {
    position: fixed;
    left: 200px;
    right: 320px;
    bottom: 32px;
    z-index: 10;
    background: transparent;
    display: flex;
    flex-direction: column;
    align-items: center;
    width: calc(100vw - 520px);
}
.banner {
    padding: 1rem;
    border-radius: 10px;
    margin: 0.5rem;
    margin-top: 0;
    flex-shrink: 0;
}
.banner-text {
    font-size: 2.7rem !important;
    line-height: 1.3 !important;
    color: #fff;
    margin-bottom: 1.2rem;
}
.banner-text ul, .banner-text li {
    font-size: 2.2rem !important;
}
.banner-text b {
    font-size: 3rem !important;
}
.reminders-container {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    margin-top: 0.5rem;
    margin-bottom: 0;
    flex-grow: 1;
    overflow-y: auto;
}
.reminders-title {
    font-size:2.2rem;font-weight:800;color:#fff;margin-top:0.5rem;margin-bottom:0.5rem;
    flex-shrink: 0;
}
.stTextArea {
    min-height: 80px;
    height: 120px !important;
    max-height: 150px;
    flex-grow: 1;
}
.file-upload-section {
    margin-bottom: 1rem;
    padding: 1rem;
    border: 2px dashed #ccc;
    border-radius: 10px;
    background-color: #f8f9fa;
}
.file-upload-section:hover {
    border-color: #666;
}
</style>
""", unsafe_allow_html=True)

