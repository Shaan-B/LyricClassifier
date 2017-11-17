from song import *
import webscraper


myLyrics = webscraper.getLyrics('Money Mitch', 'Uzi')

myLyrics.saveLyrics('myfile.txt')
newLyrics = openLyrics('myfile.txt')

print 'Title:', newLyrics.getTitle()
print 'Artist:', newLyrics.getArtist()
print 'Lyrics:', newLyrics.simpleLyrics()

print newLyrics.wordFrequencies()
