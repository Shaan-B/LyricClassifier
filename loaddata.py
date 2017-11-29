from spotipy.oauth2 import SpotifyClientCredentials
import json
import spotipy
import time
import sys
import pprint
import webscraper
import requests
import spotifyclient
import song
import os

clientid = '80c0be28d7c244148044c27a87653074'
secret = '3b7ff2e371174bd8891b51744c06488f'

def getRS500():
#Returns a dictionary of album: artist pairs
    api_path = '/songs/1779967'
    lyrics = webscraper.lyrics_from_song_api_path(api_path)
    lines = lyrics.split('\n')
    albums = {}
    for line in lines:
        if(len(line)==0): continue
        i = line.index('.') + 2
        j = line.index('(') - 1
        title = line[i:j]
        if title == 'The Beatles': title = 'White Album' #It's easier to do this
        i = line.index(' by ') + len(' by ')
        artist = line[i:]
        albums[title] = artist
    return albums

def getAlbumTracks(album, artist):
#Takes in an album/artist pair and returns a list of Song objects
#Requires artist to be an exact substring of Spotify's data
    genres = spotifyclient.getArtistGenres(artist, song.GENRES)
    client_credentials_manager = SpotifyClientCredentials(clientid, secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    sp.trace=False
    results = sp.search(q=album, limit=1, type='album')
    uri = None
    for i, t in enumerate(results['albums']['items']):
        for a in t['artists']:
            if artist in a['name']:
                uri= t
                break
    if not uri:
        return None
    item = sp.album(t['uri'])
    tracks = item['tracks']['items']
    tracknames = []
    for track in tracks:
        tracknames.append(track['name'])
    songs = []
    for track in tracknames:
        songs.append(webscraper.getSong(track, artist))
    return songs

def loaddata(destinationfolder, songlist):
#Writes songs to .pkl file and stores their metadata in songlist
    num_tracks = 0

    #rs500 = {'Yeezus': 'Kanye West', 'DAMN': 'Kendrick Lamar', '4 Your Eyez Only': 'J. Cole'}
    rs500 = getRS500()
    for album in rs500:
        print(album)
        print('\tGetting track list...')
        artistwords = rs500[album].split(' ')
        for word in artistwords:
            tracks = getAlbumTracks(album, rs500[album])
            if tracks:
                fragment = word
                break
        if not tracks:
            print('\tNot found.')
            continue
        print('\tSaving...')
        f = open(songlist, 'w+')
        for track in tracks:
            namecopy = track.title.replace(' ', '')
            name = ''
            for c in namecopy:
                if c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    name += c
            i = 1
            while os.path.isfile(os.path.join(destinationfolder, name+'.pkl')):
                name += str(i)
                i += 1
            track.saveSong(name+'.pkl', destinationfolder)
            f.write(track.title + ', ' + fragment if fragment else rs500[album] + '\n')
            num_tracks += 1
        print('\tDone.')
    print('Saved', num_tracks, 'tracks')

if __name__=='__main__':
    loaddata('rs500', 'rs500.txt')
