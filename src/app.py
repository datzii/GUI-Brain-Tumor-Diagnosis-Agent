import streamlit as st
import os
from PIL import Image
import uuid
from services.agent_service import make_query_to_agent

# Configuración de la página
# Set page configuration FIRST before anything else
st.set_page_config(
    page_icon="./resources/intelligent-assistant_12775374.png",
    page_title="Brain Tumor Diagnosis Agent",
    layout="wide"
)

# Custom CSS to move the title closer to the top
st.markdown(
    """
        <style>
                .stAppHeader {
                    background-color: rgba(255, 255, 255, 0.0);  /* Transparent background */
                    visibility: visible;  /* Ensure the header is visible */
                }

               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }

                div[class^='st-emotion-cache-10oheav'] { padding-top: 0rem; }
        </style>
        """,
    unsafe_allow_html=True,
)

#st.markdown(" <style> div[class^='st-emotion-cache-10oheav'] { padding-top: 0rem; } </style> ", unsafe_allow_html=True)
# give title to the page
st.title("🧠 Brain Tumor Diagnosis Agent")


if 'messages' not in st.session_state:
    st.session_state['messages'] = []

st.session_state.chatId = uuid.uuid4

# Sidebar con opción de ocultar
with st.sidebar:
    col1, col2 = st.columns([1, 1])  # Adjust column widths if needed

    with col1:
        if st.button("➕ New Chat"):
            st.session_state.chat_history = []
            st.session_state.chatId = uuid.uuid4()
            print(st.session_state.chatId)
            st.session_state['messages'] = []
            st.rerun()

    with col2:
        selected_option = st.selectbox(
            "Select Option",  # Label (will be hidden in sidebar)
            ["Qwen2.5", "gpt-4o-mini"],  # Options
            label_visibility="collapsed"  # Hides the label
        )
    
    st.write("## Upload MRI Image")
    uploaded_file = st.file_uploader("Upload MRI Image", type=["png", "jpg", "jpeg"], label_visibility='hidden')
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Image Previewer", use_container_width=True)


# update the interface with the previous messages
for message in st.session_state['messages']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# create the chat interface
if prompt := st.chat_input("Enter your query"):
    st.session_state['messages'].append({"role": "user", "content": prompt})
    with st.chat_message('user'):
        st.markdown(prompt)

    # get response from the model
    with st.chat_message('assistant'):
        response = st.write(make_query_to_agent(prompt))
    st.session_state['messages'].append({"role": "assistant", "content": response})

    # handle message overflow based on the model size