from song import *
import webscraper
from preProcessingUtil import *
from classifier import *
import numpy as np
import tflearn
from sklearn import preprocessing
import loadsongs
import song
from song import Song
import spotifyclient
import requests
import loaddata
from autoEncoder import *

# artist = 'Dolly Parton'
# song = 'Jolene'
# myLyrics = webscraper.getLyrics(song, artist)
#
# myLyrics.saveLyrics('music/' + song + '.txt')
# newLyrics = openLyrics('music/' + song + '.txt')
#
# #print('Title:', newLyrics.getTitle())
# #print('Artist:', newLyrics.getArtist())
# #print('Lyrics:', newLyrics.simpleLyrics())
#
# #print(newLyrics.wordFrequencies())
#
# #here are the labels, we will need to find a way to systemize labels in the future
# #labels should be a list that matches up 1-1 with the indices in data
# labels  = ['r&b', 'rap', 'rap', 'country', 'rap', 'rap']
# num_classes = 4
#
# #here is the data
# #vecotrize takes as input a list of strings, one for each song
# #it then return the same list as a tfidf vector
# #tfidf is like word fequency but it weights acording to word rarity
# onehotLabels = oneHotEncoder(num_classes, labels)
#
# data = vectorize(getMusicList())
# #print("data[0]: ", data.tolist()[0])
# #print("onehotLabels: ", onehotLabels)
#
#
#
# #makes a softmaxresolving neural network in tensrflow
# #arguments are the integer size of the input layer and the output layer
#
#
# model = modelBuilder(len(data.tolist()[0]),num_classes)
#
# # Start training (apply gradient descent algorithm)
# model.fit(data, onehotLabels, n_epoch=100, batch_size=3, show_metric=True)



# loadsongs.save('songlist.txt', 'songs')
# s = loadsongs.load('songs')
# def getLyrics(directory):
#     lyrics = []
#     labels = []
#     songs =  loadsongs.load(directory)
#     for song in songs:
#         print (song.genres)
#         lyrics.append(song.simpleLyrics())
#         labels.append(song.genres[0])
#
#     print("lyrics: ", lyrics)
#     print("labels: ", labels)
#     return lyrics, labels
#
# getLyrics('songs')
#
# #NOTE:we need to remove backslashes ann perentheses
#
# #NOTE:song.title return artist information please fix
# for e in s:
#     print ("genre testing: ", e.genres)
#
# song_title = 'The 500 Greatest Albums of All Time'
# artist_name = 'Rolling'
#
# search_url = webscraper.base_url + "/search"
# params = {'q': song_title + " " + artist_name}
# response = requests.get(search_url, params=params, headers=webscraper.headers)
# json = response.json()
# for hit in json["response"]["hits"]:
#     if artist_name.lower() in hit["result"]["primary_artist"]["name"].lower(): #requires artist_name is substring of Genius's artist name
#         print(hit["result"]["api_path"])
#         break
#
#
# #print(len(loaddata.getAlbumTracks('Yeezus', 'ye')))
#
#
# #TODO: say that a song is only pop if it doesn't fit any other genre
#
# def printGenreDistribution(songs):
#     print('Total number of songs:', len(songs))
#     genrecounts = {}
#     genrecountcounts = {}
#     nogenre = 0
#     for song in songs:
#         genrecounts[''.join(song.genres)] += 1
#         # if len(song.genres) in genrecountcounts.keys():
#         #     genrecountcounts[len(song.genres)] += 1
#     print (genrecounts)
# =======

#takes in song objects and a list of one hot encodings
def oneHotEncoder(songs):
    genresIndeces = {
    'pop' : 0,
    'rap' : 1,
    'rock' : 2,
    'r&b' : 3,
    'country' : 4,
    'edm' : 5,
    'latin' : 6,
    'jazz' : 7
    }
    encodings = []
    for song in songs:
        if(len(song.genres) >= 1):
        #     zeros  = [0,0,0,0,0,0,0,0]
        #     zeros[genresIndeces[song.genres[0]]] = 1
        # if(len(song.genres > 1)):
            hotVal = 1/len(song.genres)
            zeros  = [0,0,0,0,0,0,0,0]
            for genre in song.genres:
                zeros[genresIndeces[genre]] = hotVal
            encodings.append(zeros)
    return encodings

songs = loadsongs.load('larkin1000')
songs = [song for song in songs if(len(song.genres) >= 1)]
songs = [song for song in songs if (song.genres[0] != 'rock')]
def genreDistribution(songs):
    print('Total number of songs:', len(songs))
    genrecounts = {}
    genrecountcounts = {}
    nogenre = 0
    for song in songs:
        if len(song.genres) in genrecountcounts.keys():
            genrecountcounts[len(song.genres)] += 1
        else:
            genrecountcounts[len(song.genres)] = 1
        for genre in song.genres:
            if genre in genrecounts.keys():
                genrecounts[genre] += 1
            else:
                genrecounts[genre] = 1
    for genre in genrecounts:
        print(genre + ': ' + str(genrecounts[genre]))
    print()
    print('Number of genres:')
    for count in genrecountcounts:
        print(str(count) + ': ' + str(genrecountcounts[count]))



# print("one hots: ", oneHotEncoder(songs)[0])
# print(songs[0].title)
#print(vectorize([song.lyrics for song in songs])[0].tolist())

print(genreDistribution(songs))
data = vectorize(lyrics2POS([song.simpleLyrics() for song in songs if (len(song.genres) > 0)]), 3)
model = modelBuilder(len(data.tolist()[0]), 8)
# model, encoder = autoEncoder(len(data.tolist()[0]), 8)
# trainEncoder(np.array(data[:int(len(data) * .66)]), model, encoder)
trainX, trainY = np.array(data[:int(len(data) * .66)]), np.array(oneHotEncoder(songs)[:int(len(data) * .66)])
testX, testY = np.array(data[int(len(data) * .66):]), np.array(oneHotEncoder(songs)[int(len(data) * .66):])
print(len(testX))
model.fit(trainX, trainY, n_epoch=200, batch_size=50, show_metric=True, validation_set=(testX, testY))
# print('Total number of songs:', len(songs))
# genrecounts = {}
# genrecountcounts = {}
# nogenre = 0
# for song in songs:
#     if len(song.genres) in genrecountcounts.keys():
#         genrecountcounts[len(song.genres)] += 1
#     else:
#         genrecountcounts[len(song.genres)] = 1
#     if len(song.genres) == 0:
#         print(song.title, song.artist)
#     for genre in song.genres:
#         if genre in genrecounts.keys():
#             genrecounts[genre] += 1
#         else:
#             genrecountcounts[len(song.genres)] = 1
#         if len(song.genres) == 0:
#             print(song.title, song.artist)
#         for genre in song.genres:
#             if genre in genrecounts.keys():
#                 genrecounts[genre] += 1
#             else:
#                 genrecounts[genre] = 1
#     for genre in genrecounts:
#         print(genre + ': ' + str(genrecounts[genre]))
#     print()
#     for count in genrecountcounts:
#         print(str(count) + ': ' + str(genrecountcounts[count]))


print(loaddata.getAlbumTracks('No Secrets', 'Carly'))
