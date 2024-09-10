import streamlit as st
import google.generativeai as genai

# Configure the Generative AI API
genai.configure(api_key="Insert Your Own Api Key")

# Generation configuration for the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config
)

# Start the chat session (with an empty history for now)
chat_session = model.start_chat(
    history=[]  # Initial history is empty for now, you can customize this
)

# Set up the chat history (Session State)
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Function to handle user input and update the chat session
def send_message():
    user_message = st.session_state["user_input"]
    st.session_state['messages'].append({"user": "You", "message": user_message})
    
    # Get the bot's response
    bot_response = bot_reply(user_message)
    st.session_state['messages'].append({"user": "Bot", "message": bot_response})
    
    # Clear the input field
    st.session_state["user_input"] = ""

# Bot reply function that uses the chat session to generate a response
def bot_reply(message):
    response = chat_session.send_message(message)  # Sends the user's message to the model
    return response.text  # Return the response text from the bot

# Add custom CSS for styling
st.markdown("""
    <style>
        /* Main Chat Container */
        .chat-container {
            max-width: 700px;
            margin: 0 auto;
            padding: 20px;
            border-radius: 10px;
            background-color: #f0f2f6;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        }
        
        /* User message */
        .user-message {
            background-color: #61dafb;
            color: white;
            padding: 10px;
            border-radius: 8px;
            text-align: left;
            margin: 10px 0;
        }

        /* Bot message */
        .bot-message {
            background-color: #eceff1;
            color: black;
            padding: 10px;
            border-radius: 8px;
            text-align: left;
            margin: 10px 0;
        }

        /* Center the input */
        .stTextInput input {
            border-radius: 10px;
            padding: 10px;
            font-size: 16px;
        }
        
        /* Title Style */
        .stApp header h1 {
            color: #30475e;
            text-align: center;
            font-size: 36px;
            font-family: "Helvetica Neue", sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

# Streamlit App layout
st.title("✨ Gemini Chat App ✨")

# Container for chat
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

# Display the chat history
for chat in st.session_state['messages']:
    if chat['user'] == "You":
        st.markdown(f"<div class='user-message'><strong>You:</strong> {chat['message']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-message'><strong>Bot:</strong> {chat['message']}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Input field for user message
st.text_input("Type your message:", key="user_input", on_change=send_message)
