import webscraper

def load(listfile, destinationfolder):
#Takes in a file in the following format:
#   song1, artist1
#   song2, artist2,
#   etc.
#and loads them into pkl files in the destination folder
    f = open(listfile, 'r')
    
