import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import PunktSentenceTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
import os
from sklearn import preprocessing
import numpy as np

string = "Some people might think that traveling in a group led by a tour guide is a good way. But, a group tour normally has its strict schedule and does not offer the tourists in group any chance to meet many people in new place. So, I strongly disagree with the statement that the best way to travel is in a group led by a tour guide."
hi = "hi"

#onehot encoder
#takes as input the number of classes and the label list of the data
def oneHotEncoder(num_classes, labels):
    le = preprocessing.LabelEncoder()
    le.fit(labels)
    encodedLabels = le.transform(labels).tolist()

    a = np.array(encodedLabels)
    onehotLabels = np.zeros((len(encodedLabels), num_classes))
    onehotLabels[np.arange(len(encodedLabels)), a] = 1
    return onehotLabels

def get_document_filenames(document_path='music'):
        return [os.path.join(document_path, each) for each in os.listdir(document_path)]
#str list  -> vector list
#input song strings
#return vectorized representations ready for training
def getMusicList():
    lyricList = []
    for path in get_document_filenames():
        with open(path, 'r') as file:
            lyricList.append(file.read())
    return lyricList


def lyrics2POS(songs):
    fullPOSList = []
    for song in songs:
        words = word_tokenize(song)
        posTags = nltk.pos_tag(words)
        justTags = [tag for word, tag in posTags]
        fullPOSList.append(" ".join(justTags))
    return fullPOSList

def vectorize(tokenizedList):
    tfidfVectorizer = TfidfVectorizer(ngram_range=(1, 1), stop_words='english', analyzer='word')
    vector = tfidfVectorizer.fit_transform(tokenizedList).todense()
    #print(tfidfVectorizer.get_feature_names())
    return vector

#print("vetorized POS: ", vectorize(lyrics2POS(getMusicList())))


def preProcess(songs):
    # tfidfVectorizer = TfidfVectorizer(input='filename')
    tfidfVectorizer = TfidfVectorizer(stop_words='english', analyzer='word')
    #print(tfidfVectorizer.fit_transform(get_document_filenames()))
    print(tfidfVectorizer.fit_transform(songs).todense())
    print(tfidfVectorizer.get_feature_names())
    for song in songs:
        for sentence in [p for p in song.split('\n') if p]:
           # senTokenizer = PunktSentenceTokenizer(string)
            #sentences = senTokenizer.tokenize(string)
            #print(nltk.corpus.stopwords.words('english'))
            #for sentence in sentences:
            words = word_tokenize(sentence)
            cleanWords = [word for word in words if word not in set(nltk.corpus.stopwords.words('english'))]
            posTags = nltk.pos_tag(words)
            justTags = [tag for word, tag in posTags]

            #print(justTags)
           # print(words)
            #print("clean words: ", cleanWords)

#preProcess(getMusicList())
