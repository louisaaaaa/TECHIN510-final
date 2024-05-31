import os
import psycopg2
from dotenv import load_dotenv
import re

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

# Create table if it does not exist
cur.execute('''CREATE TABLE IF NOT EXISTS puzzle
                  (question TEXT, answer TEXT)''')

# Function to parse the text file and extract questions and answers
def parse_puzzles(file_path):
    puzzles = []
    question = ""
    answer = ""

    # Read the file line by line
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()  # Remove leading/trailing whitespace

            if line == "":  # Skip empty lines
                continue

            if "Answer:" in line:
                answer = line.removeprefix("Answer: ").strip()
                puzzles.append((question, answer))
                question = ""  # Reset question after storing
            else:
                question = re.sub(r'^\d+\.\s*', '', line).strip()

    return puzzles

# File path to the text file containing the puzzles
file_path = 'puzzles.txt'

# Parse the puzzles from the text file
puzzles = parse_puzzles(file_path)

# Insert the puzzles into the database
for question, answer in puzzles:
    cur.execute("INSERT INTO puzzle (question, answer) VALUES (%s, %s)", (question, answer))

# Commit the changes and close the connection
con.commit()
cur.close()
con.close()
