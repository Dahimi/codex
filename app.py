import streamlit as st
import requests
import json
import time

# API details
url = st.secrets["API_URL"]
headers = {
    "X-API-Key": st.secrets["API_KEY"]
}

# Sidebar info
st.sidebar.image("alpha10x_logo_c.png", use_column_width=True)
st.sidebar.info(
    "ALPHA10X Financial Codex is a specialized AI-powered system "
    "that provides insights and analysis on Saudi Arabia's finance "
    "and economy. It's designed to assist investors, analysts, and "
    "researchers with up-to-date information and trends in the Saudi market."
)
st.sidebar.warning(
    "Disclaimer: This is a demo version. The final version of the Codex will be available in Nostradamus Platform in the next release."
    "Nevertherless it reflects the actual data and expert analysis that will be provided by ALPHA10X Codex."
)

# Sidebar for credentials
st.sidebar.title("Login")

email = st.sidebar.text_input("Email")
password = st.sidebar.text_input("Password", type="password")

# Predefined authorized users (for simplicity, use a dictionary)
authorized_users = {
    "authorized@example.com": "password123"
}

# Check if the user is authorized
if st.sidebar.button("Login"):
    if (email.endswith("@kerney.com") or email.endswith("@alpha10x.ai")) and password == "password123":
        st.sidebar.success("Login successful!")
        st.session_state.authorized = True
    else:
        st.sidebar.error("Unauthorized! Please check your credentials.")
        st.session_state.authorized = False
# Only show the chatbot if the user is authorized
if st.session_state.get("authorized"):
    st.title("ALPHA10X Financial Codex")
    st.subheader("Specialized in Saudi Arabia Finance and Economy")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("What would you like to know about Saudi Arabia's finance and economy?"):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Prepare the payload for the API request
        # Prepare the chat history for the API request
        chat_history = [(msg["role"], msg["content"]) for msg in st.session_state.messages]

        payload = {
            "question": prompt,
            "chat_history": chat_history
        }

        # Make the API request and stream the response
        response = requests.post(url, json=payload, headers=headers, stream=True)

        # Display the assistant's response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    
                    if line.startswith('data: '):
                        try:
                            data = json.loads(line[6:])  # Remove 'data: ' prefix
                            if 'ops' in data:
                                for op in data['ops']:
                                    if op['op'] == 'add' and op['path'].startswith('/logs/Final_LLM/streamed_output_str/'):
                                        full_response += op['value']
                                        message_placeholder.markdown(full_response + "▌")
                        except json.JSONDecodeError:
                            pass
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

else:
    st.warning("Please log in to access the ALPHA10X Financial Codex Chatbot.")
