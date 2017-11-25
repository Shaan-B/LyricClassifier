import tflearn
from tflearn.layers.conv import conv_1d, global_max_pool

def modelBuilder(inputLayer, outputLayer):

    net = tflearn.input_data(shape=[None, inputLayer])
    net = tflearn.fully_connected(net, 100)
    net = tflearn.fully_connected(net, 75)
    net = tflearn.fully_connected(net, 50)
    net = tflearn.fully_connected(net, outputLayer, activation='softmax')




    # branch1 = conv_1d(net, 128, 3, padding='valid', activation='relu', regularizer="L2")
    # #print ("branch1:", branch1)
    #
    # branch2 = conv_1d(net, 128, 4, padding='valid', activation='relu', regularizer="L2")
    # branch3 = conv_1d(net, 128, 5, padding='valid', activation='relu', regularizer="L2")
    # net = merge([branch1, branch2, branch3], mode='concat', axis=1)
    # net = tf.expand_dims(net, 2)
    # net = global_max_pool(net)
    # net = dropout(net, 0.5)
    net = tflearn.regression(net)
    # net = fully_connected(net, nb_classes, activation='softmax')
    # net = regression(net, optimizer='adam', learning_rate=0.001,
    #                      loss='categorical_crossentropy', name='target')

    # Define model
    #model = tflearn.DNN(net)
    model = tflearn.DNN(net, tensorboard_verbose=3)
    return model
