import nltk
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import preprocessing

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
