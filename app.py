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
import nltk
from nltk.stem import WordNetLemmatizer

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

# Initialize WordNet Lemmatizer
lemmatizer = WordNetLemmatizer()

def lemmatize_input(text):
    # Tokenize the input text
    tokens = nltk.word_tokenize(text)
    # Lemmatize each token and join them back
    lemmatized_text = ' '.join([lemmatizer.lemmatize(word) for word in tokens])
    return lemmatized_text

def chat(inp):
    inp = inp.lower()  # Convert input text to lowercase
    lemmatized_input = lemmatize_input(inp)  # Lemmatize the input text
    
    # Check if the lemmatized input matches any tag
    for i in data['intents']:
        if i['tag'] == lemmatized_input:
            return np.random.choice(i['responses'])

    # If tag not found, search in patterns
    for i in data['intents']:
        for pattern in i['patterns']:
            if lemmatized_input in pattern:
                return np.random.choice(i['responses'])

    return "I'm listning please go ahead....."

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
