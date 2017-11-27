import loadsongs

loadsongs.save('songlist.txt', 'songs')
s = loadsongs.load('songs')

for e in s:
    print e.title
    
