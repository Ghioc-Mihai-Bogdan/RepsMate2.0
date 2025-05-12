import streamlit as st

st.set_page_config(page_title="Custom Menu", layout="wide")

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
    height: 85vh !important;
    overflow: hidden !important;
}
[data-testid="stAppViewContainer"] > .main {
    height: 85vh !important;
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
</style>
""", unsafe_allow_html=True)

menu_col, content_col = st.columns([1, 4])

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
        st.markdown('<div id="repsmate-title">Repscore</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        # Place the label and input in a fixed-position container
        st.markdown('<div id="bottom-chat-container">', unsafe_allow_html=True)
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

