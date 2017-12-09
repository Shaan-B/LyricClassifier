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
import os
import glob
import hdf5_getters

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
        if title == 'The Beatles': title = 'White Album'
        elif len(title) == 0: title = 'Pronounced Leh-Nerd Skin-Nerd'
        i = line.index(' by ') + len(' by ')
        artist = line[i:]
        albums[title] = artist
    return albums

def getLarkin1000():
#Returns a dictionary of album: artist pairs
#Sourced from: http://www.rocklistmusic.co.uk/virgin_1000_v3.htm
    f = open('Larkin1000.txt')
    lines = f.readlines()
    albums = {}
    for line in lines:
        nonum = line[line.index('. ')+2:]
        items = nonum.split(' - ')
        title = items[1].replace('\n', '')
        albums[title] = items[0]
    return albums

def getMillionSubset():
#Returns a dictionary of album: artist pairs
#from the Million Song Dataset subset available on columbia.edu
    albums = {}
    basedir = 'millionsubset'
    ext = '.hd5'
    subdir = basedir
    for root, dirs, files in os.walk(basedir):
        for f in files:
            try:
                f = os.path.join(root,f)
                h5 = hdf5_getters.open_h5_file_read(f)
                title = hdf5_getters.get_title(h5).decode('utf-8')
                artist = hdf5_getters.get_artist_name(h5).decode('utf-8')
                albums[title] = artist
                h5.close()
            except:
                print('Missed a file...')
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
    artistwords = artist.split(' ')
    for i, t in enumerate(results['albums']['items']):
        for a in t['artists']:
            for artistword in artistwords:
                if artistword in a['name']:
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
    return tracknames

def getTracklistLyrics(tracknames, artist, f=None):
#takes in a list of tracknames with a common artist, and
#returns a list of song objects
    songs = []
    for track in tracknames:
        if not track:
            continue
        if f:
            print('\t\tGetting ' + track + '...')
            f.write('\t\tGetting ' + track + '...\n')
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

def loadDataFromAlbums(albums, destinationfolder, songlist, logfile, droppedfile='dropped.txt'):
#Takes in a dictionary of album: artist  pairs
#Writes songs to .pkl file and stores their metadata in songlist
#Requires a log file for now. TODO: Don't require a log file
    num_tracks = 0
    log=open(logfile, 'w+')
    f = open(songlist, 'w+')
    d = open(droppedfile, 'w+')
    for album in albums:
        print(album)
        log.write(album+'\n')
        try:
            print('\tGetting track list...')
            log.write('\tGetting track list...\n')
            artistwords = albums[album].split(' ')
            artistwords = lensort(artistwords)
            for word in artistwords:
                tracks = getAlbumTracks(album, albums[album])
                if tracks:
                    print('\tFinding song lyrics...')
                    log.write('\tFinding song lyrics...\n')
                    tracks = getTracklistLyrics(tracks, word, log)
                    fragment = word
                    break
            if not tracks:
                print('\tNot found.')
                log.write('\tNot found.\n')
                continue
            print('\tSaving...')
            log.write('\tSaving...\n')
            dropped = 0
            for track in tracks:
                try:
                    namecopy = track.title.replace(' ', '')
                    name = ''
                    for c in namecopy:
                        if c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890":
                            name += c
                    i = 1
                    while os.path.isfile(os.path.join(destinationfolder, name+'.pkl')):
                        name += str(i)
                        i += 1
                    track.saveSong(name+'.pkl', destinationfolder)
                    f.write(track.title + ', ' + (fragment if fragment else albums[album]) + '\n')
                    num_tracks += 1
                except Exception:
                    dropped += 1
            print('\t' + ('*' if dropped>0 else '') + 'Dropped', dropped, 'tracks, out of', len(tracks))
            log.write('\t' + ('*' if dropped>0 else '') + 'Dropped ' + str(dropped) + ' tracks, out of ' + str(len(tracks)) + '\n')
            print('\tDone.')
            log.write('\tDone.\n')
        except Exception:
            print('\tSomething\'s wrong with that album...')
            d.write(album + ', ' + albums[album] + '\n')
    print('Saved', num_tracks, 'tracks.')
    log.write('Saved ' + str(num_tracks) + ' tracks.\n')
    log.close()
    f.close()
    d.close()

def loadDataFromSongs(songmetas, destinationfolder, songlist, logfile, droppedfile='dropped.txt'):
#Takes in a dictionary of song: artist pairs
#Writes songs to .pkl file and stores their metadata in songlist
#Requires a log file for now. TODO: Get rid of parentheses
    num_tracks = 0
    log=open(logfile, 'w+')
    f = open(songlist, 'w+')
    d = open(droppedfile, 'w+')
    dropped = 0
    lostArtists = 0
    lostLyrics = 0

    total = len(songmetas)
    count = 0
    for songmeta in songmetas:
        count += 1
        try:
            title = songmeta if '(' not in songmeta else songmeta[:songmeta.index('(')-1]
            if '[' in title:
                title = songmeta[:songmeta.index('[')-1]
            artist = songmetas[songmeta]
            if 'feat.' in artist:
                artist = artist[:artist.index('feat.')-1]
            print(title+' by '+artist+'... ('+str(count)+' of '+str(total)+')')
            log.write(title+' by '+artist+'...('+str(count)+' of '+str(total)+')'+'\n')
            print('\tFetching genres...', end='')
            log.write('\tFetching genres...')
            g = spotifyclient.getArtistGenres(artist, [])
            if g:
                print('found',len(g))
                log.write('found '+str(len(g))+' \n')
                if len(g)==0:
                    print('\tSkipping.')
                    log.write('\tSkipping...\t')
                    continue
            if not g:
                print('Artist not found.')
                log.write('Artist not found.\n')
                lostArtists += 1
                continue
            print('\tFinding lyrics...')
            log.write('\tFinding lyrics...\n')
            for word in artist.split(' '):
                song = webscraper.getSong(title, word, genres=g, notfound='replace')
                if song:
                    fragment = word
                    break
            if not song:
                lostLyrics += 1
                print('\tNot found.')
                log.write('\tNot found.')
                continue
            namecopy = song.title.replace(' ', '')
            name = ''
            for c in namecopy:
                if c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890":
                    name += c
            i = 1
            while os.path.isfile(os.path.join(destinationfolder, name+'.pkl')):
                name = str(i)
                i += 1
            song.saveSong(name+'.pkl', destinationfolder)
            f.write(song.title + ', ' + artist + '\n')
            num_tracks += 1
            print('\tSaved.')
            log.write('\tSaved.\n')
        except Exception as e:
            dropped += 1
            print('There was a problem with the song ', str(e)+':', str(type(e)))
            log.write('There was a problem with the song: ' + str(e)+': '+str(type(e))+'\n')
            d.write(songmeta +', '+songmetas[songmeta]+'\n')
    print('Saved', num_tracks, 'tracks out of', len(songmetas))
    print('\t',dropped,'tracks threw errors.')
    print('\t',lostArtists,'artists were not found.')
    print('\t',lostLyrics,'lyrics were not found.')
    log.write('Saved ' + str(num_tracks) + ' tracks out of ' + str(len(songmetas)) + '\n')
    log.write('\t' + str(dropped) +' tracks threw errors.')
    log.write('\t' +str(lostArtists) + ' artists were not found.')
    log.write('\t' +str(lostLyrics) + ' artists were not found.')
    log.close()
    f.close()
    d.close()


if __name__=='__main__':
    loadDataFromAlbums(getLarkin1000(), 'larkin1000_allgenres', 'larkin1000_allgenres.txt', 'larkin1000_allgenres.log')
