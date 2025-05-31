import streamlit as st
import os
from PIL import Image
import uuid
import tempfile
from services.agent_service import make_query_to_agent
from services.memory_service import leave_room

# Set config page
st.set_page_config(
    page_title="Brain Tumor Diagnosis Agent",  
    page_icon="🧠",                           
    layout="centered"                       
)

# Set title of the page
st.title("🧠 Brain Tumor Diagnosis Agent")

# Helper function to delete temp images
def del_image(temp_path):
    if temp_path and os.path.exists(temp_path):
        os.remove(temp_path)
        print(f"Deleted temp image: {temp_path}")  # Debugging
        st.session_state['temp_path'] = None
        st.session_state["send_image"] = False

# Helper function to change state based on checkbox
def change_send_image():
    st.session_state["send_image"] = st.session_state["checkbox"]

# Define state variables
if 'chatId' not in st.session_state:
    st.session_state.chatId = str(uuid.uuid4()) 

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

if 'temp_path' not in st.session_state:
    st.session_state['temp_path'] = None

if 'send_image' not in st.session_state:
    st.session_state['send_image'] = False  # Default is False

if "uploader_key" not in st.session_state:
    st.session_state["uploader_key"] = 1



print(f"send image: {st.session_state['send_image']}, temp_path: {st.session_state['temp_path']} chatid: {st.session_state.chatId}")

# Sidebar for new chat and model selection
with st.sidebar:
    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("➕ New Chat"):
            leave_room(st.session_state.chatId)
            st.session_state.chatId = str(uuid.uuid4())  # Reset chat ID
            st.session_state['messages'] = []
            st.session_state['temp_path'] = None  # Reset image
            st.session_state['send_image'] = False  # Reset checkbox
            st.session_state['uploaded_file'] = None  # Clear uploaded file
            st.session_state["uploader_key"] += 1
            st.rerun()

    with col2:
        selected_option = st.selectbox(
            "Select Option",  
            ["Qwen2.5", "GPT-4o-mini"],  
            label_visibility="collapsed"
        )

    st.write("## Upload MRI Image")
    uploaded_file = st.file_uploader("Upload MRI Image", 
                                     type=["png", "jpg", "jpeg"], 
                                     label_visibility='hidden',
                                     key=st.session_state["uploader_key"]
                                     )

    # Store uploaded file in session state
    if uploaded_file:
        st.session_state['uploaded_file'] = uploaded_file  # Save uploaded file
    else:
        st.session_state['uploaded_file'] = None  # Ensure it's cleared when no file is present

    # Checkbox to send image
    st.checkbox("Send image to Agent", 
                value = st.session_state['send_image'], 
                key = 'checkbox',
                on_change=change_send_image, 
                args = ()
                )

    # Update session state with checkbox value 

    if st.session_state['uploaded_file']:
        file_bytes = st.session_state['uploaded_file'].read()
        image = Image.open(st.session_state['uploaded_file'])
        st.image(image, caption="Image Preview", use_container_width=True)

        # Save temp image only if checkbox is checked
        if st.session_state["send_image"] and not st.session_state["temp_path"]:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                temp_file.write(file_bytes)
                st.session_state["temp_path"] = temp_file.name  # Save to session state
                print(f"Temp image saved: {st.session_state['temp_path']}") 

# Display chat history
for message in st.session_state['messages']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# Handle user input
if prompt := st.chat_input("Enter your query"):
    st.session_state['messages'].append({"role": "user", "content": prompt})
    with st.chat_message('user'):
        st.markdown(prompt)

    # Get response from model
    with st.chat_message('assistant'):
        chat_id = st.session_state.chatId
        temp_path = st.session_state["temp_path"]  # Use stored temp path
        engine = selected_option.lower()
        print(engine)

        with st.spinner("Processing request..."):
            response = make_query_to_agent(chat_id, prompt, engine, temp_path)
            print(f"Agent Response: {response}")  # Debugging

        st.write(response)

    # Store response in session state
    st.session_state['messages'].append({"role": "assistant", "content": response})

    # Cleanup temp file after agent processes it
    del_image(temp_path)

    st.rerun()  # Force UI update
