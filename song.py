class Song(object):
    """
    Object containing the lyrics to a single song
    Attributes:
            lyrics: string containing song lyrics
            title: string containing song title (optional)
            artist: string containing primary artist (optional)
    """

    def __init__(self, lyrics, title='', artist=''):
        self.lyrics = lyrics
        self.title = title.replace('\n', '')
        self.artist = artist.replace('\n', '')

    def getLyrics(self, f=None):
        return self.lyrics

    def getTitle(self):
        return self.title if len(self.title)>0 else None

    def getArtist(self):
        return self.artist if len(self.artist)>0 else None

    def  simpleLyrics(self):
    #Removes "[Chorus]", "[Verse X]", etc., punctuation, and newlines
        i = 0
        lyrics = self.lyrics.lower()
        removeChars = '\n(),.'
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

    def wordFrequencies(self):
    #Takes in a string of song lyrics and returns a dictionary containing
    #each unique word in the lyrics and its frequency
        words = self.simpleLyrics().split(' ')
        freq = {}
        for word in words:
            if word in freq:
                freq[word] += 1
            elif not word=='':
                freq[word] = 1
        return freq

    def saveLyrics(self, filename):
    #Saves title artist, lyrics to file at filename (creates a file if none exists)
    #NOTE: To save the entire Lyric object, use savefull()
        print(filename)
        f = open(filename, 'w+')
        f.write(self.title+'\n')
        f.write(self.artist+'\n')
        f.write(self.lyrics+'\n')
        f.close()

def openLyrics(filename):
#Returns new Lyric object with title, artist, and lyric drawn from file at filename
#NOTE: To open an entire Lyric object, use openfull()
    f = open(filename, 'r')
    contents = f.read()
    title = contents[:contents.index('\n')]
    contents = contents[contents.index('\n')+1:]
    artist = contents[:contents.index('\n')]
    lyrics = contents[contents.index('\n')+1:]
    return Song(lyrics, title, artist)
