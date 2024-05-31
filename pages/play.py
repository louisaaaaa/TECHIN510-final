import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv
import random
import psycopg2
import speech_recognition as sr

# Load environment variables
load_dotenv()

# Database connection parameters
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_SSL = os.getenv("DB_SSL")

# Connect to the Azure PostgreSQL database
con = psycopg2.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    sslmode=DB_SSL
)

# Create a cursor object
cur = con.cursor()

client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url="https://openai.ianchen.io/v1"
)

# Initialize speech recognition
recognizer = sr.Recognizer()

# Function to fetch puzzles from the database
def fetch_puzzles():
    cur.execute("SELECT question, answer FROM puzzle")
    puzzles = cur.fetchall()
    return puzzles

# Function to generate yes/no answers using ChatGPT
def generate_answer(prompt, chosen_situation):
    """Generates a yes/no answer to the given prompt using ChatGPT"""
    messages = [
        {"role": "user", "content": f"This is a situation puzzle, the situation is: {chosen_situation}. The question is: {prompt}. Please try to answer it with only yes or no. If you can't answer it with yes or no, tell me that you can't answer yes or no to that question. Try rephrasing it."}
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    answer = response.choices[0].message.content.strip().lower()
    if "yes" in answer or "no" in answer:
        return answer
    else:
        return "I can't answer yes or no to that question. Try rephrasing it."

# Function to generate score for the user's guess using ChatGPT
def generate_score(prompt, answer):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"This is a situation puzzle, the answer is: {answer}. The user's answer is: {prompt}. Please give the user the correct answer and tell them how their answer is, score their answer out of 10 and give them some advice on how to get a more accurate answer next time."}
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    my_answer = response.choices[0].message.content.strip().lower()
    return my_answer

# Function to reset the game
def reset_game():
    st.session_state.puzzle_index = None
    st.session_state.show_solution = False

# Function to start and stop recording
def record_audio():
    with sr.Microphone() as source:
        st.write("Recording...")
        audio = recognizer.listen(source)
        st.write("Recording stopped.")
    try:
        text = recognizer.recognize_google(audio)
        st.session_state.recorded_text = text  # Assign recorded text to session state variable
        return text
    except sr.UnknownValueError:
        st.error("Could not understand audio")
        return None
    except sr.RequestError as e:
        st.error(f"Error occurred; {e}")
        return None


# Main App Function
def main():
    # Initialize session state
    if 'puzzle_index' not in st.session_state:
        reset_game()
    
    # Fetch puzzles from the database
    puzzles = fetch_puzzles()

    if st.session_state.puzzle_index is None:
        st.session_state.puzzle_index = random.randint(0, len(puzzles) - 1)
    
    chosen_question, answer = puzzles[st.session_state.puzzle_index]

    # Display Situation
    st.write(chosen_question)

    # User Input for Question
    user_question = st.text_input("Ask me a yes or no question:")
    
        # Generate Answer Button
    if st.button("Ask me!"):
        if user_question:
            generated_answer = generate_answer(user_question, chosen_question)
            st.write("My Answer:", generated_answer)
        else:
            st.warning("Please enter a question!")
      
    # Start/Stop Recording Button
    if st.button("Start/Stop Recording"):
        is_recording = st.session_state.get('is_recording', False)
        if not is_recording:
            st.session_state.is_recording = True
            st.session_state.recorded_text = ""
            st.write("Recording started...")

            try:
                with sr.Microphone() as source:
                    st.write("Adjusting for ambient noise...")
                    recognizer.adjust_for_ambient_noise(source)
                    st.write("Listening for audio...")
                    audio = recognizer.listen(source)
                    st.write("Audio captured. Converting to text...")
                    text = recognizer.recognize_google(audio)
                    st.write("Text converted successfully.")
                    st.session_state.recorded_text = text
            except sr.UnknownValueError:
                st.error("Could not understand audio")
            except sr.RequestError as e:
                st.error(f"Error occurred; {e}")
            finally:
                st.session_state.is_recording = False
                st.write("Recording stopped.")
        else:
            st.session_state.is_recording = False
            st.write("Recording stopped.")

    # Display Recorded Text
    if st.session_state.get('recorded_text'):
        st.write("Recorded Text:", st.session_state.recorded_text)
        generated_answer = generate_answer(st.session_state.recorded_text, chosen_question)
        st.write("My Answer:", generated_answer)
        
        
        


    # Check Guess and Display Score
    user_answer = st.text_input("When you're ready give me your answer!")
    if st.button("Guess!"):
        if user_answer:
            generated_answer = generate_score(user_answer, answer)
            st.write("Results:", generated_answer)
            st.session_state.show_solution = True
        else:
            st.warning("Please enter your guess!")
    
    # Optionally, reveal the solution
    if st.session_state.show_solution:
        st.write("The correct answer was:", answer)
        if st.button("Play Again!"):
            reset_game()
            st.experimental_rerun()

# Run the App
if __name__ == "__main__":
    st.session_state.setdefault('is_recording', False)
    main()
