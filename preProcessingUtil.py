#import nltk
from nltk.tokenize import word_tokenize
#from nltk.tokenize import PunktSentenceTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
#import os
from sklearn import preprocessing
#import numpy as np


# def get_document_filenames(document_path='music'):
#         return [os.path.join(document_path, each) for each in os.listdir(document_path)]
# #str list  -> vector list
# #input song strings
# #return vectorized representations ready for training
# def getMusicList():
#     lyricList = []
#     for path in get_document_filenames():
#         with open(path, 'r') as file:
#             lyricList.append(file.read())
#     print("lyrics list: ", lyricList)
#     return lyricList


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
