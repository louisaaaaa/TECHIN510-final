import streamlit as st

# Main App Function
def main():
    # Centered Title
    st.markdown(
        """
        <h1 style='text-align: center;'>Situation Puzzle Game</h1>
        """,
        unsafe_allow_html=True
    )
    st.image("situation.png", caption='Are you ready?', width=10, use_column_width=True)
    st.write("Welcome! Situation puzzles, also known as lateral thinking puzzles or \"yes or no\" puzzles, are puzzles that require players to ask yes or no questions to determine what happened in a situation. Play with me, try to guess the answer and see how close you got!")
    st.write("You can navigate the website through the sidebar on the left. You can view and search all puzzles, write your own puzzle, or play the game. Enjoy!")
    st.write("Watch the video below to learn how to play👇🏻")
    st.video("play.mp4")

# Run the App
if __name__ == "__main__":
    main()
