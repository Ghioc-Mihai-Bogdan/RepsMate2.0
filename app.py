import streamlit as st

# Set Streamlit page configuration (must be first Streamlit command)
st.set_page_config(page_title="Custom Menu", layout="wide")

# Inject CSS for custom styles (menu icons, banner, separator, etc.)
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
    .banner {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem;
        margin-top: 0;
    }
    .banner-text {
        font-size: 2.7rem !important;
        line-height: 1.3 !important;
        color: #fff;
        margin-bottom: 1.2rem;
    }
    .banner-text ul, .banner-text li {
        font-size: 6.4rem !important;
    }
    .reminders-container {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        margin-top: 0.5rem;
        margin-bottom: 0;
    }
    .reminders-title {
        font-size:2.2rem;font-weight:800;color:#fff;margin-top:0.5rem;margin-bottom:0.5rem;
    }
    .stTextArea {
        min-height: 80px;
        height: 120px !important;
        max-height: 300px;
    }
    .menu-col {
        min-width: 120px;
        max-width: 180px;
    }
    .separator-col {
        display: flex;
        align-items: stretch;
        justify-content: center;
    }
    .separator-line {
        width: 2px;
        background: #d3d3d3;
        height: 1100px;
        margin: 0 auto;
        border-radius: 2px;
    }
    #repsmate-title {
        font-size: 6rem !important;
        font-weight: 700 !important;
        margin-bottom: 1.5rem;
    }
    </style>
''', unsafe_allow_html=True)

# --- PAGE NAVIGATION STATE ---
# Use session state to keep track of which page is active (main or brain)
if 'page' not in st.session_state:
    st.session_state['page'] = 'main'

def go_to_brain():
    st.session_state['page'] = 'brain'

def go_to_main():
    st.session_state['page'] = 'main'

# --- LAYOUT COLUMNS ---
# menu_col: left menu with navigation buttons
# content_col: main content area
# separator_col: vertical line separator
# banner_col: right-side banner with vision and reminders
menu_col, content_col, separator_col, banner_col = st.columns([1, 3, 0.05, 1])

# --- MENU COLUMN ---
with menu_col:
    # Navigation buttons (💬 for main, 🧠 for brain/add info)
    st.markdown('<style>.stButton > button { font-size: 8rem !important; height: 180px !important; width: 180px !important; line-height: 1 !important; }</style>', unsafe_allow_html=True)
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

# --- SEPARATOR COLUMN ---
with separator_col:
    # Vertical line to visually separate menu and content
    st.markdown('<div class="separator-line"></div>', unsafe_allow_html=True)

# --- MAIN CONTENT COLUMN ---
if st.session_state['page'] == 'main':
    with content_col:
        # Main chat UI
        st.markdown('<div class="flex-content-col">', unsafe_allow_html=True)
        st.markdown('<div>', unsafe_allow_html=True)
        # Main title
        st.markdown('<div id="repsmate-title">Repcore</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        # Chat input area (moved down by 1000px)
        st.markdown('<div id="bottom-chat-container" style="margin-top:1000px;">', unsafe_allow_html=True)
        st.markdown('<div class="big-label" style="text-align:left;">Type here</div>', unsafe_allow_html=True)
        user_input = st.text_input("Ask me", label_visibility="collapsed", key="main_chat_input")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    with content_col:
        # Add Info page UI
        st.markdown('<div class="flex-content-col">', unsafe_allow_html=True)
        st.markdown('<div>', unsafe_allow_html=True)
        st.markdown('<div id="repsmate-title">Add Info</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div style="margin-top:2rem;">', unsafe_allow_html=True)
        q = st.text_input("Question:", label_visibility="visible")
        a = st.text_input("Answer:", label_visibility="visible")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- BANNER COLUMN (RIGHT SIDE) ---
with banner_col:
    # Company Vision section
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

    # Reminders section (editable text area)
    st.markdown('<div class="reminders-container">', unsafe_allow_html=True)
    st.markdown('<div class="reminders-title">Reminders</div>', unsafe_allow_html=True)
    reminders = st.text_area("Add or edit reminders here...", key="reminders_section", height=600, label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

