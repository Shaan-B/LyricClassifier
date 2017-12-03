import tflearn
import tensorflow as tf
from tflearn.layers.conv import conv_1d, max_pool_1d
import numpy as np
#fully connected neural net
def modelBuilder(inputLayer, outputLayer):
    net = tflearn.input_data(shape=[None, inputLayer])
    net = tflearn.fully_connected(net, int(inputLayer * .75), activation="leaky_relu")
#    need to expand dimensions to use max pool
    net = tf.expand_dims(net, 2)
    net = max_pool_1d(net, int(inputLayer * .6))

    net = tflearn.fully_connected(net, int(inputLayer * .5), activation="leaky_relu")

    net = tflearn.fully_connected(net, int(inputLayer * .25), activation="leaky_relu")
    net = tflearn.fully_connected(net, outputLayer, activation='softmax')
    net = tflearn.regression(net, loss='softmax_categorical_crossentropy')
    model = tflearn.DNN(net, tensorboard_verbose=3)
    return model

#generative adversarial network, doesnt work
def gan(inputLayer, outputLayer):
    g = tflearn.input_data([None, 100, inputLayer])
    g = tflearn.lstm(g, 512, return_seq=True)
    g = tflearn.dropout(g, 0.5)
    g = tflearn.lstm(g, 512, return_seq=True)
    g = tflearn.dropout(g, 0.5)
    g = tflearn.lstm(g, 512)
    g = tflearn.dropout(g, 0.5)
    g = tflearn.fully_connected(g, outputLayer, activation='softmax')
    g = tflearn.regression(g, optimizer='adam', loss='categorical_crossentropy',
                           learning_rate=0.001)
    m = tflearn.SequenceGenerator(g,
                              seq_maxlen=50,
                              clip_gradients=5.0,
                              checkpoint_path='model_shakespeare')
    return m
def encodeAndTrain(tfidfs, poss, labels, epochs, tfidfencoder, posencoder, batch=50):
    tfidfencodings = [tfidfencoder.predict(np.array([tfidf])).tolist()[0] for tfidf in tfidfs]
    posencodings = [posencoder.predict(np.array([pos])).tolist()[0] for pos in poss]
   # newTensors = [np.append(tfidfencodings[i], (poss[i])) for i in range(len(tfidfencodings))]
    #newTensors = [np.append(tfidfs[i], (poss[i])) for i in range(len(tfidfencodings))]
    newTensors = [np.array(tfidfs[i]) for i in range(len(tfidfencodings))]

    print len(tfidfencodings[1])
   # model = modelBuilder(len(tfidfencodings[1]) + len(poss[0]), 10)
   # model = modelBuilder(len(tfidfs[0]) + len(poss[0]), 10)
    tf.reset_default_graph()

    model = modelBuilder(len(tfidfs[0]), 10)
    model.fit(np.array(newTensors), labels, n_epoch=epochs, show_metric=True, batch_size=batch)
    return model 


#rnn
#def rnn(inputLayer, outputLayer):
#    net = tflearn.input_data([None, inputLayer])
#    net = tflearn.embedding(net, input_dim=10000, output_dim=128)
#    net = tflearn.lstm(net, 128, dropout=0.8)
#    net = tflearn.fully_connected(net, outputLayer, activation='softmax')
#    net = tflearn.regression(net) #, optimizer='adam', learning_rate=0.001,
#                         #loss='categorical_crossentropy')
#    model = tflearn.DNN(net, tensorboard_verbose=3)
#    return model
#
#def fit(model):
#    return
