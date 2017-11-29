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

#Better name for this file would be loadRS500.py. Oh well.

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
        name = track['name']
        if '-' in name:
            name = name[:name.index('-')]
        if name not in tracknames:
            tracknames.append(name)
    songs = []
    for track in tracknames:
        songs.append(webscraper.getSong(track, artist))
    return songs

def lensort(a):
#Helper function
    n = len(a)
    for i in range(n):
        for j in range(i+1,n):
            if len(a[i]) < len(a[j]):
                temp = a[i]
                a[i] = a[j]
                a[j] = temp
    return a

def loaddata(destinationfolder, songlist, logfile):
#Writes songs to .pkl file and stores their metadata in songlist
#Requires a log file for now. TODO: Don't require a log file
    num_tracks = 0
    log=open(logfile, 'w+')

    #rs500 = {'Yeezus': 'Kanye West', 'DAMN': 'Kendrick Lamar', '4 Your Eyez Only': 'J. Cole'}
    rs500 = getRS500()
    for album in rs500:
        print(album)
        log.write(album+'\n')
        print('\tGetting track list...')
        log.write('\tGetting track list...\n')
        artistwords = rs500[album].split(' ')
        artistwords = lensort(artistwords)
        for word in artistwords:
            tracks = getAlbumTracks(album, rs500[album])
            if tracks:
                fragment = word
                break
        if not tracks:
            print('\tNot found.')
            log.write('\tNot found.\n')
            continue
        print('\tSaving...')
        log.write('\tSaving...\n')
        f = open(songlist, 'w+')
        dropped = 0
        for track in tracks:
            try:
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
            except Exception:
                dropped += 1
        if dropped>0:
            print('\tDropped', dropped, 'tracks, out of', len(tracks))
            log.write('\tDropped ' + str(dropped) + ' tracks, out of ' + str(len(tracks)) + '\n')
        print('\tDone.')
        log.write('\tDone.\n')
    print('Saved', num_tracks, 'tracks.')
    log.write('Saved ' + str(num_tracks) + ' tracks.\n')
    log.close()
    f.close()

if __name__=='__main__':
    loaddata('rs500', 'rs500.txt', 'rs500.log')
