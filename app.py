import streamlit as st
import pickle
import numpy as np
import speech_recognition as sr
import pyttsx3
import threading
import queue

# Load chatbot model
with open('chatbot_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Initialize text-to-speech engine
engine = pyttsx3.init()
speech_queue = queue.Queue()

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

# Function for voice input
def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Speak something...")
        audio_data = recognizer.listen(source)
        st.write("Audio input received, processing...")
        try:
            text = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            text = "Sorry, I couldn't understand what you said."
        return text

# Function to process text-to-speech requests
def process_speech_queue():
    while True:
        text = speech_queue.get()
        engine.say(text)
        engine.runAndWait()
        speech_queue.task_done()

# Start the speech processing thread
speech_thread = threading.Thread(target=process_speech_queue)
speech_thread.daemon = True
speech_thread.start()

# Streamlit UI
st.title("👨‍⚕️👨‍⚕️ Friendly Medical Chatbot")

# Display greeting message
st.write(greeting_message)

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
    speech_queue.put(response)
