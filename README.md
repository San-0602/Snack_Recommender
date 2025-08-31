🍫 Snack Recommender

A fun and interactive web app that suggests snacks based on your mood and time of day. Complete with subtle floating particles, colorful vibes, and cheeky comments for each snack!

🚀 Features

Suggests snacks tailored to your mood (happy, sad, bored, angry, excited, stressed).

Considers the time of day (morning, afternoon, evening, night, midnight).

Displays sarcastic or witty comments alongside snack suggestions.

Interactive, minimalistic UI with subtle floating colorful particles.

Fully built with Python, Flask, and scikit-learn.

🛠️ Installation

Clone the repo:

git clone <repo_url>
cd snack-recommender


Install dependencies:

pip install -r requirements.txt


Run the Flask app:

python app.py


Open your browser and go to:

http://127.0.0.1:5000

🧠 How It Works

A Decision Tree Classifier is trained on a dataset of moods, times, and corresponding snacks.

Encoders handle categorical data for moods, times, and snacks.

When you select your mood and time, the app predicts a snack and fetches a witty comment.

Floating colorful particles in the background keep the interface lively but not distracting.
