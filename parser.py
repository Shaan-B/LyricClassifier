import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
from nltk.tag import pos_tag_sents
brown_ic = wordnet_ic.ic('ic-brown.dat')

moneymitch = open('music/moneymitch.txt')
# for i in moneymitch.readlines():
#     print (i)
