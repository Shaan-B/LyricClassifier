import requests
import locale
from bs4 import BeautifulSoup

#Do not change!
base_url = "http://api.genius.com"
headers = {'Authorization': 'Bearer nmTRwnDzAujQLr3voLlJhjAfty-sDacg89_vyGhFC7seVLdi5oeKlurmQzB2J9hF'}

def lyrics_from_song_api_path(song_api_path):
    song_url = base_url + song_api_path
    response = requests.get(song_url, headers=headers)
    json = response.json()
    path = json["response"]["song"]["path"]
    #gotta go regular html scraping... come on Genius
    page_url = "http://genius.com" + path
    page = requests.get(page_url)
    html = BeautifulSoup(page.text, "html.parser")
    #remove script tags that they put in the middle of the lyrics[h.extract() for h in html('script')]
    #at least Genius is nice and has a tag called 'lyrics'!
    lyrics = html.find("div", class_ = "lyrics").get_text() #updated css where the lyrics are based in HTML
    return lyrics.encode('utf-8')

def getLyrics(song_title='Wanted You', artist_name ='Nav'):
    search_url = base_url + "/search"
    params = {'q': song_title + " " + artist_name}
    response = requests.get(search_url, params=params, headers=headers)
    json = response.json()
    song_info = None
    for hit in json["response"]["hits"]:
        if artist_name.lower() in hit["result"]["primary_artist"]["name"].lower(): #requires artist_name is substring of Genius's artist name
            song_info = hit
            break
    if song_info:
        song_api_path = song_info["result"]["api_path"]
        return lyrics_from_song_api_path(song_api_path)
    else:
        return None

#Removes "Chorus", "Verse X", etc. identifiers and newlines
def removeExtras(lyrics):
    i = 0
    while i < len(lyrics): #I think this is bad practice. w/e
        c = lyrics[i]
        if c == '\n':
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

print removeExtras(getLyrics())
