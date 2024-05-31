import streamlit as st
import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection parameters
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_SSL = os.getenv("DB_SSL")

# Function to connect to the database
def connect_to_db():
    try:
        connection = psycopg2.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            sslmode=DB_SSL
        )
        cursor = connection.cursor()
        return connection, cursor
    except (Exception, psycopg2.Error) as error:
        st.error("Error while connecting to PostgreSQL")
        st.error(error)

# Function to create a new puzzle entry in the database
def create_puzzle(situation, answer):
    connection, cursor = connect_to_db()
    if connection:
        try:
            cursor.execute("INSERT INTO puzzle (question, answer) VALUES (%s, %s)", (situation, answer))
            connection.commit()
            st.success("Puzzle entry created successfully")
        except (Exception, psycopg2.Error) as error:
            st.error("Error while inserting data to PostgreSQL")
            st.error(error)
        finally:
            if connection:
                cursor.close()
                connection.close()

# Main App Function
def main():
   
        st.title("Write Your Own Puzzle!")
        new_situation = st.text_input("Enter the situation:")
        new_answer = st.text_input("Enter the answer:")
        if st.button("Submit"):
            if new_situation and new_answer:
                create_puzzle(new_situation, new_answer)
            else:
                st.warning("Please enter both situation and answer.")


if __name__ == "__main__":
    main()
