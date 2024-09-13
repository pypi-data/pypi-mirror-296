import pickle
import joblib
import importlib.resources as pkg_resources  # New import for loading bundled files
import numpy as np
from gensim.models import Word2Vec

class SentimentModel:
    def __init__(self):
        # Automatically load the model and vectorizer from the package
        self.model = self.load_model()
        self.word2vec = self.load_vectorizer()  # Using Word2Vec
        self.label_mapping = {
            0: "negative",
            1: "positive"
        }

    def load_model(self):
        # Load the model file from the package data
        with pkg_resources.open_binary('sentiment_analysis', 'Logistic_model.pkl') as file:
            return pickle.load(file)

    def load_vectorizer(self):
        # Load the Word2Vec model from the package data
        with pkg_resources.open_binary('sentiment_analysis', 'vectorizer.pkl') as file:
            return joblib.load(file)

    def preprocess_text(self, text):
        # Handle common negations
        text = text.replace("not a bad", "good")
        text = text.replace("not bad", "good")
        text = text.replace("not good", "bad")
        text = text.replace("n't", " not")
        # Add more preprocessing as necessary
        return text

    def predict(self, text: str):
        # Preprocess the input text
        processed_text = self.preprocess_text(text)
        
        # Convert the input text to Word2Vec embeddings
        words = processed_text.split()  # Split text into words
        word_vectors = [self.word2vec.wv[word] for word in words if word in self.word2vec.wv]
        
        if not word_vectors:
            raise ValueError("None of the words in the text are present in the Word2Vec model vocabulary")
        
        # Calculate the mean of the word vectors to get a single feature vector
        text_transformed = np.mean(word_vectors, axis=0).reshape(1, -1)
        
        # Predict using the trained classifier
        prediction = self.model.predict(text_transformed)[0]
        confidence = self.model.predict_proba(text_transformed)

        return f"{self.label_mapping.get(prediction, 'unknown')}"
