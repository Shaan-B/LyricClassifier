from __future__ import division, print_function, absolute_import

import numpy as np
import nltk
import string
import itertools
import matplotlib.pyplot as plt
import pickle
import tflearn

from sklearn.metrics import confusion_matrix
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from collections import Counter
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import shuffle
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score




import tflearn
import pickle
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from sklearn import svm

from tflearn.data_utils import to_categorical, pad_sequences
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import shuffle
from keras.preprocessing.text import Tokenizer, text_to_word_sequence
from tflearn.layers.conv import conv_1d, global_max_pool
from tflearn.layers.merge_ops import merge
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.embedding_ops import embedding
from tflearn.layers.estimator import regression

def nueralnetwork(padlen, model, depth = 0, windowRanges = [3, 4, 5]):
    # Building convolutional network
    tf.reset_default_graph()
    sess = tf.Session()

    network = input_data(shape=[None, padlen], name='input')

    network = tflearn.embedding(network, input_dim=1000, output_dim=128)
    if model == 'CNN':
        print("___________CNN____________")
        branches = [conv_1d(network, 128, window, padding='valid', activation='relu', regularizer="L2") for window in windowRanges]
        network  = merge(branches, mode='concat', axis=1)
        network = tf.expand_dims(network, 2)
        network = global_max_pool(network)
        network = dropout(network, 0.5)

    if model == 'RNN':
        print("___________RNN_____________")
        network = tflearn.lstm(network, 128, dropout=0.8)

    network = fully_connected(network, nb_classes, activation='softmax')
    network = regression(network, optimizer='adam', learning_rate=0.001,
                         loss='categorical_crossentropy', name='target')

    writer = tf.summary.FileWriter(LOGDIR)
    writer.add_graph(sess.graph)
    return network

def trainAndTest(network, tags, labels, padlen):
    print("training")
    # Data preprocessing
    accuracy_score = []
    recall = []
    precision = []
    f1 = []
    # Data preprocessing
    X, Y = tags, labels

    sess = tf.Session()
    sess.run(tf.global_variables_initializer())
    writer = tf.summary.FileWriter("ouput")
    writer.add_graph(sess.graph)

    for i in range(1, 2):
      X, Y = shuffle(X, Y, random_state=i)

      trainX = X[:-250]
      testX = X[-250:]

      trainY = Y[:-250]
      testY = Y[-250:]

      print(testY)
      print(testY[0])

      # Sequence padding
      trainX = pad_sequences(trainX, maxlen=padlen, value=0.)
      testX = pad_sequences(testX, maxlen=padlen, value=0.)
      # Converting labels to binary vectors
      trainY = to_categorical(trainY, nb_classes=nb_classes)
      testY = to_categorical(testY, nb_classes=nb_classes)

      # Training
      model = tflearn.DNN(network, tensorboard_verbose=3)
      model.fit(trainX, trainY, n_epoch = 2, shuffle=True, validation_set=(testX, testY), show_metric=True, batch_size=32)

      accuracy_score += model.evaluate(testX, testY)

     ##format##
    #   recall += recall_score(trainY, model.predict(trainX), average="weighted")
    #   precision += precision_score(trainY, model.predict(trainX), average="weighted")
    #   f1 += f1_score(trainY, model.predict(trainX), average="weighted")


    return accuracy_score


