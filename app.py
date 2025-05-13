import streamlit as st

st.set_page_config(page_title="Custom Menu", layout="wide")

# Inject highly specific CSS for menu icon buttons at the very top
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

st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    height: 100vh !important;
    overflow: auto !important;
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
}
.separator-line {
    width: 2px;
    background: #d3d3d3;
    height: 1100px;
    margin: 0 auto;
    border-radius: 2px;
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
    left: 0;
    right: 0;
    bottom: 32px;
    z-index: 10;
    background: transparent;
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100vw;
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
}
.reminders-title {
    font-size:2.2rem;font-weight:800;color:#fff;margin-top:0.5rem;margin-bottom:0.5rem;
}
.stTextArea {
    min-height: 80px;
    height: 120px !important;
    max-height: 150px;
}
</style>
""", unsafe_allow_html=True)

menu_col, content_col, separator_col, banner_col = st.columns([1, 3, 0.05, 1])

with menu_col:
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

if st.session_state['page'] == 'main':
    with content_col:
        st.markdown('<div class="flex-content-col">', unsafe_allow_html=True)
        st.markdown('<div>', unsafe_allow_html=True)
        st.markdown('<div id="repsmate-title">Repcore</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        # Place the label and input in a fixed-position container
        st.markdown('<div id="bottom-chat-container" style="margin-top:1000px;">', unsafe_allow_html=True)
        st.markdown('<div class="big-label" style="text-align:left;">Type here</div>', unsafe_allow_html=True)
        user_input = st.text_input("Ask me", label_visibility="collapsed", key="main_chat_input")
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    with content_col:
        st.markdown('<div class="flex-content-col">', unsafe_allow_html=True)
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

