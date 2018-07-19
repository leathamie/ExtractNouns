#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 07:59:39 2018

@author: lea
"""

import re
import nltk
import nltk.tokenize

def extractFileContent(filename):
    fileContent = ""
    file = open(filename, "r")
    for line in file : 
        fileContent = fileContent + line
    return fileContent


def getSpeechLines(filePath):
    content = extractFileContent(filePath)
    line_tab = re.findall('\*[A-Z]+:.*_[0123456789][0123456789]*', content)
    print (len(line_tab))
    return line_tab

def splitLines(speechLines):
    lines = []
    for line in speechLines:
        splitLine = splitOneLine(line)
        if len(splitLine) != 0:
            lines.append(splitLine)

    return lines

def splitOneLine(line):
    #print (line)
    line = line.split(':\t')
    act = line[0]
    act = act.replace('*','')
    #print(act)
    line = line[1]
    line = line.split('\x15')
    sentence = line[0]
    sentence = cleanSentence(sentence)
    if sentence == "" or sentence == " " :
        return []
    else:
        line = line[1]
        line = line.split('_')
        on = line[0]
        off = line[1]
        #print ("sentence "+sentence)
        #print ("on " + on)
        #print ("off "+ off)
        return [act, on, off, sentence]

def cleanSentence(sentence):
    sentence = re.sub('\[.*\]','',sentence)
    sentence = re.sub("[^a-zA-Z ']",'',sentence)
    sentence = sentence.lower()
    sentence = re.sub('xxx','',sentence)
    sentence = re.sub('  +','',sentence)
    return sentence

def getFileName(filePath):
    filename = filePath.split('/')[-1]
    if len(filename) == 0 :
        filename =filePath.split('.')[0]
    else : 
        filename = filename.split('.')[0]
    return filename
    
def saveInFile(filePath):
        lines = getSpeechLines(filePath)
        print (lines)
        contentTab = splitLines(lines)
        filename = getFileName(filePath)
        file = open(filename + '.txt','w')
        file.write('name,on,off,sentence,POSnouns,Ojects\n')
        #print ("len de contentTab" + str(len(contentTab)))
        for content in contentTab:
            content = addNouns(content)
            content = addObj(content)
            content = tabToString(content)
            file.write(content)

def tabToString(lineTab):
    line = ""
    print ("len de linTab : " + str(len(lineTab)))
    for i in range (0,len(lineTab)):
        if len(lineTab)-1 == i:
            line = line + lineTab[i] + '\n'
        else:
            line = line + lineTab[i] + ','
    return line 
        

def addNouns(line):
    nouns = getNouns(line[3])
    line.append(nouns)
    return line

def addObj(line):
    obj = getObj(line[3])
    line.append(obj)
    return obj
    

def getNouns(sentence):
    nouns = ""
    sentence = nltk.tokenize.word_tokenize(sentence)
    pos_sentence = nltk.pos_tag(sentence)
    print (pos_sentence)
    for elt in pos_sentence:
        if elt[1] == 'NN' or elt[1] == 'NNS':
            if nouns != "":
                nouns = nouns + " "
            nouns = nouns + elt[0]
    print (nouns)
    return nouns


def getObj(sentence):
    obj = ""
    matchSentences = ["can you get the", "the ","that is a ","and the ","a ","it is a ","this is a ","and a ","can you say ","here is the ","and ","where is the ","that is the ","look at the ","i have the ","you want the ","color is the ","is that the ","there is the ","you put the ","to put the ","one is the "]
    for matchSentence in matchSentences:
        matchResults = re.findall(matchSentence + '[a-z]+',sentence)
        for match in matchResults:
            match = match.replace(matchSentence,'')
            if obj != "":
                obj = obj + " "
            obj = obj + match 
    print("object  = " + obj)
    return obj
    


        
def getAllSpeechDuration(filename):
    content = extractFileContent(filename)
    duration_tab = re.findall('[0123456789][0123456789]*_[0123456789][0123456789]*', content)
    return duration_tab
            
def getBigining(filename):
    content = extractFileContent(filename)
    m = re.search('[0123456789][0123456789]*_[0123456789][0123456789]*', content)
    first_duration = m.group(0)
    on = first_duration.split('_')[0]
    return on

def getEnd(filename):
    content = extractFileContent(filename)
    last_duration = re.findall("[0123456789][0123456789]*_[0123456789][0123456789]*", content)[-1]
    off = last_duration.split('_')[1]
    print(off)
    return off


lines = saveInFile('/home/lea/Stage/DATA/chaFiles/Rollins/nb09.cha')


