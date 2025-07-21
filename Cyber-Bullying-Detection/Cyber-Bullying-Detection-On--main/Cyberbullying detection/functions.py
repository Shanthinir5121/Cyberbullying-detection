import nltk
nltk.download('stopwords')
import pandas as pd
import numpy as np
import re
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay

import pandas as pd
import numpy as np
import re
import string
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from nltk.tokenize import RegexpTokenizer
from nltk import PorterStemmer, WordNetLemmatizer
import pickle


def data_processing(tweet):
    tweet = re.sub("\d*\.\d+","",str(tweet)) # convert numbers present to strings --decimal number
    tweet = re.sub("\d+","",str(tweet)) # convert numbers present to strings-- just number
    tweet = tweet.lower()
#     tweet = re.sub(r"https\S+|www\S+http\S+", '', tweet, flags = re.MULTILINE) #replace https with null-> ''
    tweet = re.sub(r"((www.[^s]+)|(http\S+))","",tweet,flags = re.MULTILINE)
    tweet = re.sub(r'\@w+|\#','', tweet)
    tweet = re.sub("\d*\.\d+","",tweet)
    tweet =  re.sub(r'(\w)\1{2,}', r'\1\1', tweet) #booooookkkkkkkkk
    tweet = re.sub(r'[^\w\s]','',tweet) #This line of code removes all non-word and non-space
    tweet = re.sub(r'ð','',tweet)
    tweet_tokens = word_tokenize(tweet)
    filtered_tweets = [w for w in tweet_tokens if not w in stop_words]
    return " ".join(filtered_tweets)

 # similar but different frop stemming by considering the literal meaning of the word

def lemmatizing(text):
    lemmatizer = WordNetLemmatizer()
    tokens = nltk.word_tokenize(text)
    lemmatized_tokens = [lemmatizer.lemmatize(token, pos='v') for token in tokens]
    lemmatized_text = ' '.join(lemmatized_tokens)
    return lemmatized_text
    
    
    
    
def custom_input_prediction(text):
    import nltk
    nltk.download('omw-1.4')
    #print(text)
    #text = pd.Series(text)
    #print(text)
    text = str(data_processing(text))
    print(text)
    text = [text]
    print(text)
    vectoriser = pickle.load(open("vectorizer", "rb"))
    text = vectoriser.transform(text)
    loaded_topchi2 = np.load('topchi2.npy')
#     X_train_chi2 = X_train[:, topchi2]
    text = text[:,loaded_topchi2]
    model = pickle.load(open("logreg", "rb"))
#     model = pickle.load(open("svm", "rb"))
    prediction = model.predict(text)
    #print(prediction)
    prediction = prediction[0]
    #print(prediction)
    interpretations = {
        0 : "not bully",
        1 : "bully"
      
    }

    for i in interpretations.keys():
        if i == prediction:
            return interpretations[i]
    