#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 07:59:39 2018

@author: lea
"""

import re
import nltk
import nltk.tokenize
from nltk import pos_tag, word_tokenize
from nltk.corpus import wordnet as wn 

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
        for line in splitLine : 
            if len(line) != 0:
                lines.append(line)
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
    sentences = cleanSentence(sentence)
    lines = []
    line = line[1]
    line = line.split('_')
    on = line[0]
    off = line[1]
    for sentence in sentences:
        if sentence != "" and sentence != " " :
            #print ("sentence "+sentence)
            #print ("on " + on)
            #print ("off "+ off)
            lines.append([act, on, off, sentence])
    return lines


def cleanSentence(sentence):
    sentence = sentence.replace("[/]","\n")
    sentences = sentence.split("\n")
    cleanSentences = []
    for sentence in sentences:
        sentence = re.sub('\[.*\]','',sentence)
        sentence = re.sub("[^a-zA-Z ']",'',sentence)
        sentence = sentence.lower()
        sentence = re.sub('xxx','',sentence)
        sentence = re.sub('  +',' ',sentence)
        cleanSentences.append(sentence)
    return cleanSentences

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
    #print ("line  = " + str(line) + " , obj = " + obj)
    line.append(obj)
    #print ("line after append obj : " + str(line))
    return line
    

def getNouns(sentence):
    nouns = ""
    sentence = word_tokenize(sentence)
    pos_sentence = nltk.pos_tag(sentence)
    for elt in pos_sentence:
        if elt[1] == 'NN' or elt[1] == 'NNS':
            if nouns != "":
                nouns = nouns + " "
            nouns = nouns + elt[0]
    return nouns


def getObj(sentence):
    obj = ""
    matchSentences = ["can you get the ", "the ", "da ","that is a ","that's a ","and the ","a ","it is a ","this is a ","and a ","can you say ","here is the ","and ","where is the ","that is the ","look at the ","i have the ","you want the ","color is the ","is that the ","there is the ","you put the ","to put the ","one is the "]
    for matchSentence in matchSentences:
        matchResults = re.findall(' ' +matchSentence + '[a-z]+',sentence)
        for match in matchResults:
            match = match.replace(' ' + matchSentence,'')
            if obj != "":
                if len(re.findall(match,obj)) == 0:
                    obj = obj + " "
                    obj = obj + match 
            else :
                obj = obj + match 
    return obj

def get_obj_by_POS_and_sentences(sentence):
    list_obj1 = getObj(sentence)
    list_obj2 = getNouns(sentence)
    list_obj1 = list_obj1.split(" ")
    list_obj2 = list_obj2.split(" ")
    return list(set(list_obj1).intersection(list_obj2))
    

################################  
def ratioObjectsMatch(filePath):
    text = getTextFromCha(filePath)
    objList = getObj(text).split(" ")
    objDic = cleanObjList(objList)
    objDic = set_ratio_each_obj_foud_notFoud(text, objDic)
    ratio = getTotalRatio(objDic)
    print ("proportion trouvée en moyenne : " + str(ratio))
    return ratio
    
def perfObjMatch(arg):
    obj = "bigbird birdie cow piggy bird box baby book bear glasses kitty bunny firetruck hat stuff pie sheep boat piggie rings babys rug"
    obj = obj.split(" ")
    nbObjToFind = len (obj)
    objNotFound = obj
    text = getTextFromCha('/home/lea/Stage/DATA/chaFiles/Rollins/nb09.cha')
    
    if arg == 1 :
        objFound = getNouns(text).split(" ")
        cat = "NLTK POS tagging "
    elif arg == 3 :
        objFound = get_obj_by_POS_and_sentences(text)
        cat = "Union NLTK POS tagging and sentences"
    else : 
        objFound = getObj(text).split(" ")
        cat = "Typical sentences "
    
    objFound = cleanObjList(objFound)
    objFound = set_ratio_each_obj_foud_notFoud(text, objFound)
    
    countObjFound = 0
    meanRatio = 0.0
    print ("-----" + cat + "-----")
    for elt in objFound:
        if elt['object'] in  obj:
            meanRatio = meanRatio + elt['ratio']
            objNotFound.remove(elt['object'])
            countObjFound += 1
        
        else : 
            print ("Mots en trop : " + elt['object'])
    print ("matchobj / solution : " + str(countObjFound/nbObjToFind))
    print ("precison nb de mots qui sont des objets / nombre d'objets trouvés : " + str(countObjFound/len(objFound)) )
    print ("moyenne des précisions(nombre de fois ou le mot est trouvé / le nombre de fois où il apparait : " + str(meanRatio /countObjFound))
    print ("Not found objects : " + str(objNotFound))
  

def getTotalRatio(objDic):
    ratio = 0.0
    for obj in objDic:
        ratio = ratio + obj['ratio']
    ratio = ratio /len(objDic)
    print (ratio)
    return ratio

def getTextFromCha(filePath):
    lines = getSpeechLines(filePath)
    txt = ""
    for line in lines:
        if txt != "":
            txt = txt + ". "
        splittedLine = splitOneLine(line)
        if len (splittedLine) >0:
            txt = txt + splittedLine[0][3]
    txt = txt.replace(" .",".")
    txt = re.sub("\.+",".", txt)
    return (txt)
    
def set_ratio_each_obj_foud_notFoud(text, objDic):
    for obj in objDic:
        nb  = len (re.findall(obj['object'], text))
        nb = float(obj['nbfound']/nb)
        obj['ratio'] = nb
    return objDic
        
def cleanObjList(objList):
    dicList = []
    for i in range (0, len(objList)):
        obj = objList[i]
        n = 0
        for j in range(0, len(objList)):
            if obj == objList[j]:
                if j < i:
                    break
                else:
                    n = n + 1
        if n > 0:
            dicList.append({'object' : obj, 'nbfound' : n, 'ratio': 0})
    return dicList
    
    

################################       
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

#lines = saveInFile('/home/lea/Stage/DATA/chaFiles/Rollins/nb09.cha')

#ratioObjectsMatch('/home/lea/Stage/DATA/chaFiles/Rollins/nb09.cha')

perfObjMatch(1)
perfObjMatch(2)
perfObjMatch(3)
    
#sentence = getTextFromCha('/home/lea/Stage/DATA/chaFiles/Rollins/nb09.cha')
#print (get_obj_by_POS_and_sentences(sentence))