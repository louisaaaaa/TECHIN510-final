# TECHIN510-final-Situation-Puzzle-Game
Interested in mystery stories? Enjoy using your critical thinking skills to solve problems?
This website game is for you! 
"A man is found dead in an empty room, with only a pool of water nearby... How did he die?"
Ask me questions to find out more about the situation and solve the mystery!
Or come up with your own situation and let other players guess!

## Technologies used
- Streamlit
  - Multiple pages
  - Video player
  - Search bar
- ChatGPT API
- Azure postgreSQL database
- Google speech-to-text recognition API


## What problems am I trying to solve
- I want to create a fun and interactive game for users to enjoy
- I want to use better prompting techniques to get desired output
- I want to be able to store and search puzzles
- I want to add speech-to-text for better user experience
   
## How to Run
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run how_to_play.py
```

## Reflections
### What I learned
- How to use streamlit to create a web application
- How to use GPT APIs to generate text
- How to improve prompts to get desired output
- How to use database to store and retrieve information
- How to use voice recognition to get user input
- How to use pictures to improve UI
### What questions/problems did I face
- I tried to scrape data from the web, but most websites have anti-scraping measures and I failed to do so
- I could run the voice recognition on my local machine, but not on the server, streamlit cloud does not support it https://discuss.streamlit.io/t/error-installing-pyaudio-for-voice-processing/63630/3
  
