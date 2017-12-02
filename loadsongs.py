import webscraper
import os
import sys
from song import Song
import _pickle as pickle

def save(listfile, destinationfolder):
#Takes in a file in the following format:
#   song1, artist1
#   song2, artist2, notfound, optionalgenre1, optionalgenre2
#   song3, artist3, notfound
#   etc.
#and loads them into pkl files in the destination folder
    #try:
        f = open(listfile, 'r')
        contents = f.read()
        songs = contents.split('\n')
        for song in songs:
            items = song.split(', ')
            s = None
            if len(items) == 2:
                s = webscraper.getSong(items[0], items[1])
            elif len(items) > 2:
                s = webscraper.getSong(items[0], items[1], items[2], items[3:])
            if s:
                namecopy = s.title.replace(' ', '')
                name = ''
                for c in namecopy:
                    if c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890":
                        name += c
                i = 1
                while os.path.isfile(os.path.join(destinationfolder, name+'.pkl')):
                    name += str(i)
                    i += 1
                s.saveSong(name+'.pkl', destinationfolder)
    # except Exception as e:
    #     print('Somthing went wrong...')
    #     print(e)

def load(folder, genres=[]):
#Takes in a folder and returns a list of Song objects from the .pkl files it contains
    songs = []
    try:
        for f in os.listdir(folder):
            if f.endswith('.pkl'):
                s = Song.openSong(os.path.join(folder, f))
                s.filter(genres)
                if len(s.genres)>0:
                    songs.append(s)
        return songs
    except Exception as e:
        print('Somthing went wrong...')
        print(e)

def convertPKLto2(folder, newfolder):
    songs = load(folder)
    for song in songs:
        namecopy = song.title.replace(' ', '')
        name = ''
        for c in namecopy:
            if c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890":
                name += c
        i = 1
        while os.path.isfile(os.path.join(newfolder, name+'.pkl')):
            name += str(i)
            i += 1
        filename = os.path.join(newfolder, name)+'.pkl'
        f = open(filename, 'wb+')
        pickle.dump(song, f, protocol=2)

if __name__ == '__main__':
    path = None
    sub = 'songs'
    if len(sys.argv) > 0:
        path = sys.argv[0]
    if len(sys.argv) > 1:
        sub = sys.argv[1]
    elif os.path.exists('songlist.txt'):
        path = 'songlist.txt'
    if path:
        save(path, sub)
