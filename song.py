import spotifyclient
import _pickle as pickle
from nltk.tokenize import word_tokenize
import os

GENRES = {
'pop': 'POP',
'rap': 'RAP',
'rock': 'RCK',
'r&b': 'RNB',
'country': 'CNT',
'edm': 'EDM',
'latin': 'LTN',
'jazz': 'JZZ',
}

class Song(object):
    """
    Object containing the lyrics to a single song
    Attributes:
            lyrics: string containing song lyrics
            genres: list containing genres
            title: string containing song title (optional)
            artist: string containing primary artist (optional)
    """

    def __init__(self, lyrics, title='', artist='', notfound='ignore'):
    #Constructor takes in local variables and option if genre is not found thru Spotify client
        self.lyrics = lyrics
        self.title = title.replace('\n', '')
        self.artist = artist.replace('\n', '')
        self.genres = genres if notfound=='add' else []
        #if (len(genres)==0) or notfound=='add':
        print('doing it')
        print(self.artist)
        artistgenres = spotifyclient.getArtistGenres(self.artist, GENRES.keys())
        print(artistgenres)
        if artistgenres:
            for g in artistgenres:
                self.genres.append(g)
        elif notfound == 'prompt':
            genres = raw_input('Genres not found, please input: ').split(',')
            if len(genres) > 0:
                self.genres = genres

    def tokens(self):
        return word_tokenize(self.simpleLyrics())

    def  simpleLyrics(self):
    #Removes "[Chorus]", "[Verse X]", etc., punctuation, and newlines
        i = 0
        lyrics = self.lyrics.lower()
        removeChars = '\n'
        while i < len(lyrics): #I think this is bad practice. w/e
            c = lyrics[i]
            if c in removeChars:
                lyrics = lyrics[:i] + ' ' + lyrics[i+1:]
            elif c=='[':
                j = 1
                while lyrics[i+j]!=']':
                    j += 1
                if j<50: #Safety check in case bracket isn't matched
                    lyrics = lyrics[:i]+lyrics[i+j+1:]
            else:
                i+=1
        return lyrics

    def tokenFrequencies(self):
    #Takes in a string of song lyrics and returns a dictionary containing
    #each unique word in the lyrics and its frequency
        lyrics = self.simpleLyrics()
        words = word_tokenize(lyrics)
        freq = {}
        for word in words:
            if word in freq:
                freq[word] += 1
            elif not word=='':
                freq[word] = 1
        return freq

    def saveLyrics(self, filename):
    #Saves title artist, lyrics to file at filename (creates a file if none exists)
    #NOTE: To save the entire Song object, use saveSong()
        f = open(filename, 'w+')
        f.write(self.title+'\n')
        f.write(self.artist+'\n')
        f.write(self.lyrics+'\n')
        f.close()

    def saveSong(self, filename, subdirectory=''):
    #Saves Song object to file at filename, which can include a subdirectory
        if len(subdirectory) == 0:
            f = open(filename, 'wb+')
        else:
            try:
                os.mkdir(subdirectory)
            except Exception:
                pass
            f = open(os.path.join(subdirectory, filename), 'wb+')
        pickle.dump(self, f)

    @staticmethod
    def openLyrics(filename):
    #Returns new Song object with title, artist, and lyric drawn from file at filename
    #NOTE: To open an entire Lyric object, use openSong()
        f = open(filename, 'r')
        contents = f.read()
        title = contents[:contents.index('\n')]
        contents = contents[contents.index('\n')+1:]
        artist = contents[:contents.index('\n')]
        lyrics = contents[contents.index('\n')+1:]
        return Song(lyrics, title, artist)

    @staticmethod
    def openSong(filename):
    #Returns a new Song object with all data drawn from filename
        f = open(filename, 'rb')
        return pickle.load(f)
