#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 08:19:04 2018

@author: lea
"""
import nltk
import nltk.tokenize
sentence1 = "here can we put the green one on ."
sentence2 = "let's see if we can stack the [/] the rings ."

text = nltk.tokenize.word_tokenize(sentence2)
print (nltk.pos_tag(text))
