import pickle
import pandas as pd
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import pandas as pd

def preprocess_text(text):
    token = word_tokenize(text.lower())
    swords = stopwords.words('english')
    tokens = [word for word in token if word.isalnum() and word not in swords]
    wnl = WordNetLemmatizer()
    return [wnl.lemmatize(word) for word in tokens]


def classify_text_domain(text):
    # processed_text = preprocess_text(text)
    # with open("vectorizer.pkl", "rb") as file:
    #     vectorizer = pickle.load(file)
    # text_vector = vectorizer.transform([processed_text])
    # with open("news_classifier.pkl", "rb") as file:
    #     model = pickle.load(file)
    # prediction = model.predict(text_vector)
    return 'India'
