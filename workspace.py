from song import *
import webscraper
from vectorizer import *
import numpy as np
import tflearn
from sklearn import preprocessing


# myLyrics = webscraper.getLyrics('Money Mitch', 'Uzi')
#
# myLyrics.saveLyrics('myfile.txt')
# newLyrics = openLyrics('myfile.txt')
#
# print('Title:', newLyrics.getTitle())
# print('Artist:', newLyrics.getArtist())
# print('Lyrics:', newLyrics.simpleLyrics())
#
# print(newLyrics.wordFrequencies())

#here are the labels, we will need to find a way to systemize labels in the future
#labels should be a list that matches up 1-1 with the indices in data
labels  = ['rap', 'essay', 'pop']
num_classes = 3
le = preprocessing.LabelEncoder()
le.fit(labels)
encodedLabels = le.transform(labels).tolist()

#onehot encoder

a = np.array(encodedLabels)
onehotLabels = np.zeros((len(encodedLabels), num_classes))
onehotLabels[np.arange(len(encodedLabels)), a] = 1


#here is the data
#vecotrize takes as input a list of strings, one for each song
#it then return the same list as a tfidf vector
#tfidf is like word fequency but it weights acording to word rarity

data = vectorize(getMusicList())
print("data[0]: ", data.tolist()[0])
print("onehotLabels: ", onehotLabels)






net = tflearn.input_data(shape=[None, len(data.tolist()[0])])
net = tflearn.fully_connected(net, 100)
net = tflearn.fully_connected(net, 50)
net = tflearn.fully_connected(net, num_classes, activation='softmax')
net = tflearn.regression(net)

# Define model
model = tflearn.DNN(net)
# Start training (apply gradient descent algorithm)
model.fit(data, onehotLabels, n_epoch=10, batch_size=16, show_metric=True)
