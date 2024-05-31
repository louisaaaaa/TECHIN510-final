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

# Function to fetch all puzzles from the database
def fetch_all_puzzles():
    connection, cursor = connect_to_db()
    puzzles = []
    if connection:
        try:
            cursor.execute("SELECT * FROM puzzle")
            puzzles = cursor.fetchall()
        except (Exception, psycopg2.Error) as error:
            st.error("Error while fetching data from PostgreSQL")
            st.error(error)
        finally:
            if connection:
                cursor.close()
                connection.close()
    return puzzles

# Main App Function
def main():
    st.title("Search or View All Puzzles!")

    # Search Bar
    search_query = st.sidebar.text_input("Search Puzzles")

    # View All Puzzles Page
    puzzles = fetch_all_puzzles()
    if puzzles:
        for puzzle in puzzles:
            if search_query.lower() in puzzle[0].lower() or search_query.lower() in puzzle[1].lower():
                expander_title = f"Question: {puzzle[0]}"
                with st.expander(expander_title, expanded=False):
                    st.write(f"Answer: {puzzle[1]}")
                    st.write("--------------------")
    else:
        st.info("No puzzles found in the database")

if __name__ == "__main__":
    main()
