import tflearn
from tflearn.layers.conv import conv_1d, global_max_pool

def modelBuilder(inputLayer, outputLayer):

    net = tflearn.input_data(shape=[None, inputLayer])
    net = tflearn.fully_connected(net, int(inputLayer * .75))
    net = tflearn.fully_connected(net, int(inputLayer * .5))
    net = tflearn.fully_connected(net, int(inputLayer * .25))
    net = tflearn.fully_connected(net, outputLayer, activation='softmax')
    net = tflearn.regression(net)
    model = tflearn.DNN(net, tensorboard_verbose=3)
    return model
