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

#test name -> (text, labels, # ofclasses) "X,Y"
# string -> (list, list, int)

LOGDIR = "/tmp/mnist_tutorial/"

def preProcess(TEST, features, classifier='NN'):



# udp and also POS

#corpus, input features, type of model, modelfeature -- # of layers, window, paddding
#epochs

#also able to record what parameters where used
#two things ive learned two things on confised about

    #For true modularity we should standerdize the names
    #tags and label documents. tags.txt and labels.txt
    #seems fine as long as they are in the correct folders

    if TEST == 'CAES':
        if features == 'POS':
            POS = open('../NLI/CAES/Data/POS_tags.txt', 'r')
            lang = open('../NLI/CAES/Data/labels.txt','r') #does tags.txt == POStags
        if features == 'UDP':
            POS = open('../NLI/CAES/Data/UDP_tags.txt', 'r')
            lang = open('../NLI/CAES/Data/UDP_labels_nli.txt','r') #standardize this document
        #if features == 'kernels':

        #still need tree kernels stl and stu

    if TEST == 'FCE':
        #if features == 'POS':

        if features == 'UDP':
            POS = open('../NLI/FCE/Data/UDP_tags_nli.txt', 'r')
            lang = open('../NLI/FCE/Data/UDP_labels_nli.txt','r')

    if TEST == 'TOEFL':
        #if features == 'UDP':

        if features == 'POS':
            print("got it")
            POS = open('../NLI/TOEFL/Data/UDP_tags_nli.txt', 'r')
            lang = open('../NLI/TOEFL/Data/UDP_labels_nli.txt','r')



    POS_list = POS.readlines()
    print("POS_list: ",POS_list[0])
    POS_list = [x.strip() for x in POS_list]
    print("POS_list: ",POS_list[0])
    #tknzr = Tokenizer(lower=False, split=" ")
    tknzr = Tokenizer(lower=True, split=" ")
    tknzr.fit_on_texts(POS_list)
    #two dimentional array of essay converted intor part of speech tags
    #list

    # X = [8, 3, 1, 3, 6, 4, 10, 6, 3, 1, 4, 10, 3, 1, 8, 3, 7,
    # 9, 1, 7, 5, 1, 4, 2, 2, 3, 1, 6, 7, 3, 1, 4], [], [] ....]

    X = tknzr.texts_to_sequences(POS_list)
    print ("X:", X)
    lang_list = lang.readlines()
    lang_list = [x.strip() for x in lang_list]
    le = LabelEncoder()

    #one dimmentional array that has number values for each label
    #i.e spanish = 1, russian = 2 etc
    #Y = [ 0  0  0 ..., 15 15 15]
    Y = le.fit_transform(lang_list)

    class_names = list(le.classes_)
    #create a set of all uniques values in the labels list
    #turn that set into a list and output its length as the number
    # of unique language labels
    #6 for CAES, 11 for TOEFL
    print("done")
    print("bundle:",len(list(set(lang_list))) )
    if classifier == 'SVM':
        svm = TfidfVectorizer(ngram_range=(1, 3), norm='l2').fit_transform(POS_list).toarray()
        return (svm,Y,len(list(set(lang_list))), class_names)
    return (X,Y,len(list(set(lang_list))), class_names)


def nueralnetwork(padlen, model, depth = 0, windowRanges = [3, 4, 5]):
    # Building convolutional network
    tf.reset_default_graph()
    sess = tf.Session()

    network = input_data(shape=[None, padlen], name='input')

    network = tflearn.embedding(network, input_dim=1000, output_dim=128)
    #print ("network:", network)
    if model == 'CNN':
        print("CNNnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn=======================================================================")
        branches = [conv_1d(network, 128, window, padding='valid', activation='relu', regularizer="L2") for window in windowRanges]
        network  = merge(branches, mode='concat', axis=1)
        #branch1 = conv_1d(network, 128, 3, padding='valid', activation='relu', regularizer="L2")
        #print ("branch1:", branch1)

    #    branch2 = conv_1d(network, 128, 4, padding='valid', activation='relu', regularizer="L2")
        #branch3 = conv_1d(network, 128, 5, padding='valid', activation='relu', regularizer="L2")
        #network = merge([branch1, branch2, branch3], mode='concat', axis=1)
        network = tf.expand_dims(network, 2)
        network = global_max_pool(network)
        network = dropout(network, 0.5)









    if model == 'RNN':
        print("RNN=======================================================================")
    # Network building
    #network = tflearn.input_data([None, 100])
    #network = tflearn.embedding(net, input_dim=10000, output_dim=128)
        network = tflearn.lstm(network, 128, dropout=0.8)
    #network = tflearn.fully_connected(network, nb_classes, activation='softmax')
    #network = tflearn.regression(network, optimizer='adam', learning_rate=0.001,
    #                         loss='categorical_crossentropy')

    network = fully_connected(network, nb_classes, activation='softmax')
    network = regression(network, optimizer='adam', learning_rate=0.001,
                         loss='categorical_crossentropy', name='target')

    writer = tf.summary.FileWriter(LOGDIR)
    writer.add_graph(sess.graph)
    return network














def SVM(tags, labels, class_names):
    X, y = shuffle(tags, labels, random_state=1)

    svc2 = svm.SVC(C=1, kernel='linear', decision_function_shape='ovr')
    y_pred = svc2.fit(X[:-100], y[:-100]).predict(X[-100:]) #, y[-100:]))
    y_test = y[-100:]
    np.set_printoptions(precision=2)

    cnf_matrix = confusion_matrix(y_test, y_pred)
    print(cnf_matrix)
    pickle.dump(svc2, open( "save.p", "wb" ))

    print (classification_report(y_test, y_pred, target_names=class_names))

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    # print(cm)

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')






















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


TEST = 'TOEFL' #input('Test:')
print("==================")
print("Network Parameters")
print("==================")
padding = 150 #input('Padding:')

X,Y,nb_classes, class_names = preProcess('CAES', 'POS')
#X,Y,nb_classes, class_names = preProcess(TEST,'POS', classifier='SVM')
print (trainAndTest(nueralnetwork(int(padding), 'CNN'), X, Y, int(padding)))


#print (trainAndTest(nueralnetwork(150, 'CNN'), X, Y, 150))
#pickle.dump(accuracy_score,open( "1DCNN_" + TEST + "_" + padding, "wb" ))

#SVM(X, Y, class_names)
# # Compute confusion matrix
# np.set_printoptions(precision=2)
#
# # print (cnf_matrix)
# # Plot non-normalized confusion matrix
# plt.figure()
# plot_confusion_matrix(cnf_matrix, classes=class_names,
#                       title='Confusion matrix, without reduction')
#
# # Plot normalized confusion matrix
# # plt.figure()
# # plot_confusion_matrix(cnf_ae_matrix, classes=class_names,
# #                       title='AEd confusion matrix')
#
# plt.show()
