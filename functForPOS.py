#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 08:19:04 2018

@author: lea
"""
import nltk
import nltk.tokenize
from nltk.corpus import wordnet as wn

word1 = "bigbird birdie cow piggy bird box baby book bear glasses kitty bunny firetruck hat stuff pie sheep boat piggie rings babys rug music orange blue police"
sentence2 = "let's see if we can stack the [/] the rings ."


toy = wn.synsets('toy')
print (toy[0].definition())
obj = wn.synsets('object')
print (obj[0].definition())
print(str(toy[0].path_similarity(obj[0])))
word1= word1.split(' ')

for elt in word1:
    syns = wn.synsets(elt)
    if len(syns)>0:
        print(elt )
        print("similarité avec objet " + str(syns[0].path_similarity(obj[0])))
        print("similarité avec toy " + str(syns[0].path_similarity(toy[0])))


