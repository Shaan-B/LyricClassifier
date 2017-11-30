from song import *
import webscraper
from preProcessingUtil import *
from classifier import modelBuilder
import numpy as np
import tflearn
from sklearn import preprocessing
import loadsongs
import song
from song import Song
import spotifyclient
import requests

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

song_title = 'The 500 Greatest Albums of All Time'
artist_name = 'Rolling'

search_url = webscraper.base_url + "/search"
params = {'q': song_title + " " + artist_name}
response = requests.get(search_url, params=params, headers=webscraper.headers)
json = response.json()
for hit in json["response"]["hits"]:
    if artist_name.lower() in hit["result"]["primary_artist"]["name"].lower(): #requires artist_name is substring of Genius's artist name
        print(hit["result"]["api_path"])
        break


#print(len(loaddata.getAlbumTracks('Yeezus', 'ye')))


#TODO: say that a song is only pop if it doesn't fit any other genre


def printGenreDistribution():
    songs = loadsongs.load('oldRS500/rs500')
    print('Total number of songs:', len(songs))
    genrecounts = {}
    genrecountcounts = {}
    nogenre = 0
    for song in songs:
        if len(song.genres) in genrecountcounts.keys():
            genrecountcounts[len(song.genres)] += 1
        else:
            genrecountcounts[len(song.genres)] = 1
        if len(song.genres) == 0:
            print(song.title, song.artist)
        for genre in song.genres:
            if genre in genrecounts.keys():
                genrecounts[genre] += 1
            else:
                genrecounts[genre] = 1
    for genre in genrecounts:
        print(genre + ': ' + str(genrecounts[genre]))
    print()
    for count in genrecountcounts:
        print(str(count) + ': ' + str(genrecountcounts[count]))

print(spotifyclient.getArtistGenres('Kanye', song.GENRES))
