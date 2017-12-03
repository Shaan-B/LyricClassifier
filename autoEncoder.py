import numpy as np
import matplotlib.pyplot as plt
import tflearn


def autoEncoder(inputLayer, outputLayer):
    # Building the encoder
    encoder = tflearn.input_data(shape=[None, inputLayer])
    encoder = tflearn.fully_connected(encoder, int(inputLayer * .6))
    encoder = tflearn.fully_connected(encoder, int(inputLayer * .4))

    # Building the decoder
    decoder = tflearn.fully_connected(encoder, int(inputLayer * .6))
    decoder = tflearn.fully_connected(decoder, inputLayer, activation='sigmoid')

    # Regression, with mean square error
    net = tflearn.regression(decoder, optimizer='adam', learning_rate=0.001,
                             loss='mean_square', metric=None)
    model = tflearn.DNN(net, tensorboard_verbose=3)
    encoding_model = tflearn.DNN(encoder)
    return model, encoding_model

#x in the data input (tf-idf)
def trainEncoder(X, model, encoder):
    # Training the auto encoder
    print "x shape: ", X.shape
    model.fit(X, X, n_epoch=20, run_id="auto_encoder",
                    batch_size=256, show_metric=True)


    # Encoding X[0] for test
    print("\nTest encoding of X[0]:")
    # New model, re-using the same session, for weights sharing
    print(encoder.predict([X[0]]))
    return model
