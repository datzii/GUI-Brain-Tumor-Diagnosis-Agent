import streamlit as st
from PIL import Image
import time  # For loading simulation

# Page Configuration
st.set_page_config(page_title="Brain Tumor Diagnosis AI", layout="wide")

# ---- SIDEBAR (Chat History) ----
st.sidebar.title("📜 Conversation History")
if "messages" not in st.session_state:
    st.session_state["messages"] = []  # Store chat history

for msg in st.session_state["messages"]:
    with st.sidebar:
        st.markdown(f"🗨️ **User:** {msg['user']}")
        st.markdown(f"🤖 **AI:** {msg['ai']}")

# ---- MAIN CHATBOT AREA ----
st.title("🧠 Brain Tumor Diagnosis Chatbot")
st.write("Upload an MRI image, and chat with the AI for diagnosis.")

# File Uploader for MRI Image
uploaded_file = st.file_uploader("📂 Upload MRI Image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Chat Input
    user_input = st.text_input("Ask about your diagnosis:", "")

    if st.button("Send"):
        if user_input:
            with st.chat_message("user"):
                st.markdown(user_input)
            
            # Simulate AI Processing
            with st.chat_message("assistant"):
                with st.spinner("Analyzing..."):
                    time.sleep(2)  # Simulated AI response delay
                    ai_response = "Based on the image, there is a high probability of a tumor. Consult a specialist."
                    st.markdown(ai_response)
                    
                    # Store conversation in history
                    st.session_state["messages"].append({"user": user_input, "ai": ai_response})
