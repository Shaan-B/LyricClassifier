import tflearn
import tensorflow as tf
from tflearn.layers.conv import conv_1d, max_pool_1d

#fully connected neural net
def modelBuilder(inputLayer, outputLayer):

    net = tflearn.input_data(shape=[None, inputLayer])
    net = tflearn.fully_connected(net, int(inputLayer * .75))
    #need to expand dimensions to use max pool
    net = tf.expand_dims(net, 2)
    net = max_pool_1d(net, int(inputLayer * .6))

    net = tflearn.fully_connected(net, int(inputLayer * .5))

    net = tflearn.fully_connected(net, int(inputLayer * .25))
    net = tflearn.fully_connected(net, outputLayer, activation='softmax')
    net = tflearn.regression(net)
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
