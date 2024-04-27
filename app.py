import json
import numpy as np
import os
import warnings
import contextlib
from flask import Flask, render_template, request
from tensorflow import keras
import pickle
import colorama
from colorama import Fore, Style

warnings.filterwarnings("ignore")
colorama.init()

# Initialize Flask app
app = Flask(__name__)
app.static_folder = 'static'

# Load chatbot data
with open('train.json') as file:
    data = json.load(file)

# Load trained model
model = keras.models.load_model('chat-model.h5')

# Load tokenizer object
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

# Load label encoder object
with open('label_encoder.pickle', 'rb') as enc:
    lbl_encoder = pickle.load(enc)

# Parameters
max_len = 20

def chat(inp):
    inp = inp.lower()  # Convert input text to lowercase
    # Redirecting output to nul
    with open(os.devnull, 'w') as devnull:
        with contextlib.redirect_stdout(devnull):
            result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]), truncating='post', maxlen=max_len), verbose=0)
            tag = lbl_encoder.inverse_transform([np.argmax(result)])

    for i in data['intents']:
        if i['tag'] == tag:
            return np.random.choice(i['responses'])


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_response():
    userText = request.args.get('msg')
    print("Input sentence:", userText)
    print("Input sentence type:", type(userText))  # Add this line for debugging
    if isinstance(userText, str):  # Check if userText is a string
        response = chat(userText)
        return response
    else:
        return "Invalid input"


# Run the app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
