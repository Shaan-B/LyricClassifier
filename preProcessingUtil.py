import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import PunktSentenceTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
import os
from sklearn import preprocessing
import numpy as np

def oneHotEncoder(songs):
    genresIndeces = {
    'pop' : 0,
    'rap' : 1,
    'rock' : 2,
    'r&b' : 3,
    'country' : 4,
    'jazz' : 5,
    'blues' : 6,
    'gospel' : 7,
    'reggae' : 8,
    'electronic' : 9
    }
    encodings = []
    for song in songs:
        if(len(song.genres) >= 1):
        #     zeros  = [0,0,0,0,0,0,0,0]
        #     zeros[genresIndeces[song.genres[0]]] = 1
        # if(len(song.genres > 1)):
            hotVal = 1/len(song.genres)
            zeros  = [ 0 for i in range(len(genreIndeces))]
            for genre in song.genres:
                zeros[genresIndeces[genre]] = hotVal
            encodings.append(zeros)
    return encodings

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
    print("lyrics list: ", lyricList)
    return lyricList


def lyrics2POS(songs):
    fullPOSList = []
    for song in songs:
        words = word_tokenize(song)
        posTags = nltk.pos_tag(words)
        justTags = [tag for word, tag in posTags]
        fullPOSList.append(" ".join(justTags))
    return fullPOSList

def vectorize(tokenizedList, rang):
    #print(tokenizedList[0])
    tfidfVectorizer = TfidfVectorizer(ngram_range=(1, rang), stop_words='english', analyzer='word')
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
