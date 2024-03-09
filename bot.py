import streamlit as st
import pickle
import numpy as np
import pyttsx3
import threading
from pocketsphinx import LiveSpeech

# Load chatbot model
with open('chatbot_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine_lock = threading.Lock()

# Define greeting message
greeting_message = "Hello! How can I assist you today?"

# Define greetings, common questions, and responses
greetings = ["hi", "hello", "hey"]
common_questions = ["how are you", "what's your name", "what is your name", "who are you"]
common_responses = {
    "how are you": "I'm doing well, thank you!",
    "what's your name": "My name is Gladwin.",
    "what is your name": "My name is Gladwin.",
    "who are you": "I'm Gladwin, a friendly medical chatbot, here to assist you with medical inquiries."
}

# Function to get response from chatbot
def get_response(input_text):
    # Check for greetings
    if input_text.lower() in greetings:
        return "Hi there! How can I help you?"
    # Check for common questions
    elif input_text.lower() in common_questions:
        return common_responses[input_text.lower()]
    else:
        # If not, use chatbot model
        return model.predict([input_text])[0]

# Function for text-to-speech
def speak(text):
    global engine_lock
    with engine_lock:
        engine.say(text)
        engine.runAndWait()

# Function to stop the Streamlit app
def stop_streamlit():
    st.experimental_rerun()

# Streamlit UI
st.title("👨‍⚕️👨‍⚕️ Friendly Medical Chatbot")

# Display greeting message
st.write(greeting_message)

# Function for voice input
def voice_input():
    st.write("Speak something...")
    for phrase in LiveSpeech():
        text = str(phrase)
        return text

# Text input for user queries
user_input = st.text_input("Type your query here: ")

# Button for voice input
if st.button("Speak"):
    voice_text = voice_input()
    st.write("You said:", voice_text)
    user_input = voice_text

# Get response from chatbot
if user_input:
    response = get_response(user_input)
    st.write("Bot:", response)
    speak(response)

# Button to stop the Streamlit app
if st.button("Stop"):
    stop_streamlit()
