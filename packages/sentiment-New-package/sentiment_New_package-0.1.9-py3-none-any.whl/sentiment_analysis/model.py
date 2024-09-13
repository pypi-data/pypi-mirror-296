# import numpy as np

# class SentimentModel:
#     def __init__(self):
#         # Automatically load the model and vectorizer from the package
#         self.model = self.load_model()
#         self.vectorizer = self.load_vectorizer()
#         self.label_mapping = {
#             0: "negative",
#             1: "positive"
#         }

#     def load_model(self):
#         # Load the model file from the package data
#         with pkg_resources.open_binary('sentiment_analysis', 'classifier.pkl') as file:
#             return pickle.load(file)

#     def load_vectorizer(self):
#         # Load the Word2Vec model from the package data
#         with pkg_resources.open_binary('sentiment_analysis', 'model_word.pkl') as file:
#             return joblib.load(file)

#     def predict(self, text: str):
#         # Convert the input text to a vector by averaging word vectors
#         words = text.split()  # Split text into words
#         word_vectors = [self.vectorizer.wv[word] for word in words if word in self.vectorizer.wv]
        
#         if not word_vectors:
#             raise ValueError("None of the words in the text are present in the Word2Vec model vocabulary")
        
#         # Calculate the mean of the word vectors to get a single feature vector
#         text_transformed = np.mean(word_vectors, axis=0).reshape(1, -1)
        
#         # Predict using the trained classifier
#         prediction = self.model.predict(text_transformed)[0]
        
#         return f"Your review is {self.label_mapping.get(prediction, 'unknown')}"


import re
import pickle
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
import importlib.resources as pkg_resources  # New import for loading bundled files

class SentimentModel:
    def __init__(self):
        # Automatically load the model and vectorizer from the package
        self.model = self.load_model()
        self.vectorizer = self.load_vectorizer()
        self.label_mapping = {
            0: "negative",
            1: "positive"
        }

    def load_model(self):
        # Load the model file from the package data
        with pkg_resources.open_binary('sentiment_analysis', 'sentiment_model.pkl') as file:
            return pickle.load(file)

    def load_vectorizer(self):
        # Load the vectorizer file from the package data
        with pkg_resources.open_binary('sentiment_analysis', 'vectorizer.pkl') as file:
            return joblib.load(file)

    # def predict(self, text: str):
    #     text_transformed = self.vectorizer.transform([text])
    #     prediction = self.model.predict(text_transformed)[0]
    #     return f"Your review is {self.label_mapping.get(prediction, 'unknown')}"
    #     # Inside the SentimentModel class



    

    def preprocess_text(self,review):
        # Handling negations (this can be expanded with more cases)
        review = re.sub(r'\bnot a bad\b', 'good', review)
        review = re.sub(r'\bnot\b', 'not_', review)
        return review

    # In your predict method
    def predict(self, review):
        review = self.preprocess_text(review)
        features = self.vectorizer.transform([review])
        prediction = self.model.predict(features)
        confidence = self.model.predict_proba(features)
        
        print(f"Prediction: {prediction}, Confidence: {confidence}")
        if max(confidence[0]) < 0.6:
            return "Your review is unknown"
        elif prediction == 1:
            return "Your review is positive"
        else:
            return "Your review is negative"

        def predict(self, review):
            # Preprocess the review and get features
            features = self.vectorizer.transform([review])
            
            # Get the prediction probabilities or labels
            prediction = self.model.predict(features)
            confidence = self.model.predict_proba(features)
            
            print(f"Prediction: {prediction}, Confidence: {confidence}")
            
            # Assuming you're using confidence scores to determine "unknown"
            if max(confidence[0]) < 0.6:  # Adjust threshold as needed
                return "Your review is unknown"
            elif prediction == 1:
                return "Your review is positive"
            else:
                return "Your review is negative"

