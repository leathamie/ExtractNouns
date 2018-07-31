#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 07:59:39 2018

@author: lea
"""

import re
import os
import nltk
import nltk.tokenize
import argparse
from nltk import word_tokenize

def extractFileContent(filename):
    """
        take a cha file path and return a str with cha content
    """
    fileContent = ""
    file = open(filename, "r")
    for line in file : 
        fileContent = fileContent + line
    return fileContent


def getSpeechLines(filePath):
    """
        take a chafile path return a tab with only speech lines
    """
    content = extractFileContent(filePath)
    # regular expression for speech lines
    line_tab = re.findall('\*[A-Z]+:.*_[0123456789][0123456789]*', content)
    return line_tab

def splitLines(speechLines):
    """
        take a tab with all speech lines of a file in str, return a tab with 
        all speech lines in a tab : [Speaker, SpeechStart, SpeechEnd, Speech]
        And the all speech is cleaned
    """
    lines = []
    for line in speechLines:
        splitLine = splitOneLine(line)
        for line in splitLine : 
            if len(line) != 0:
                lines.append(line)
    return lines

def splitOneLine(line):
    """
        take a speech line (str) and return a tab with :
        speaker, speechStart, SpeechEnd, speechCleaned
    """
    line = line.split(':\t')
    act = line[0]
    act = act.replace('*','')
    line = line[1]
    line = line.split('\x15')
    sentence = line[0]
    sentences = cleanSentence(sentence)#Clean Speech; can become empty( ex: sentence = "[-]" cleanedSentence = "")
    lines = []
    line = line[1]
    line = line.split('_')
    on = line[0]
    off = line[1]
    for sentence in sentences:
        if sentence != "" and sentence != " " : #if cleaned sentence not empty
            lines.append([act, on, off, sentence])
    return lines # return tab line, can be an empty tab if cleaned sentence is empty


def cleanSentence(sentence):
    """
        clean a cha sentence, return only the speech or empty str if there is no speech
    """
    sentence = sentence.replace("[/]","\n")
    sentences = sentence.split("\n")
    cleanedSentences = []
    for sentence in sentences:
        sentence = re.sub('\[.*\]','',sentence)
        sentence = re.sub("[^a-zA-Z ']",'',sentence)
        sentence = sentence.lower()
        sentence = re.sub('xxx','',sentence)
        sentence = re.sub('  +',' ',sentence)
        cleanedSentences.append(sentence)
    return cleanedSentences

def getFileName(filePath):
    """
        take a file path and return only the file name without the extension
    """
    filename = filePath.split('/')[-1]
    if len(filename) == 0 :
        filename =filePath.split('.')[0]
    else : 
        filename = filename.split('.')[0]
    return filename
    
            
def writeFileWithAllObject(chaFilePath):
    """
        take a cha file a create a txt file with clean text and obj list
        like :  speakerName, speechStart,speechEnd, Speech, objectsFound
    """
    text = getTextFromCha(chaFilePath) # get a str with the speech only
    objFound = get_obj_by_POS_and_sentences(text) # get a list of objects found in the speech
    filename = getFileName(chaFilePath)
    file = open("DATA/" + filename + '.txt','w')
    lines = getSpeechLines(chaFilePath) # get a tab with speech lines 
    contentTab = splitLines(lines) # split the lines to a tab with speaker, speechStart, speechEnd, speech 
    file.write('name,on,off,sentence,Objects\n')
    for content in contentTab: #Browse the speech lines 
        objList = "" # str for obj found in a sentence
        for elt in objFound: # Browe all the found objects in the speech
            if " " + elt in content[3]: #if the object is in the sentence. Without the " " before elt, the elt "hat" is found in "what" 
                if objList != "": 
                    objList += " "
                objList += elt
        content.append(objList)
        content = tabToString(content) # convert a tab to a str separated by ","
        file.write(content) # write the line to the txt file
    

def tabToString(lineTab):
    """
        Take a tab and return a str with all the table cells separated by ','
    """
    line = ""
    for i in range (0,len(lineTab)):
        if len(lineTab)-1 == i:
            line = line + lineTab[i] + '\n'
        else:
            line = line + lineTab[i] + ','
    return line 
        


def getNouns(sentence):
    """
        Take a sentence (str), retrurn the nouns singular or plural using 
        NTLK POS tag
    """
    nouns = ""
    sentence = word_tokenize(sentence)
    pos_sentence = nltk.pos_tag(sentence)
    for elt in pos_sentence:
        # NN for singular nouns and NNS for plural nouns
        if elt[1] == 'NN' or elt[1] == 'NNS':
            if nouns != "":
                nouns = nouns + " "
            nouns = nouns + elt[0]
    return nouns


def getObj(sentence):
    """
        take  a sentence and return a tab with words who appear 
        in a specific place in tipical sentences
    """
    obj = ""
    #List of words or phrases that can be preceded by an object name 
    matchSentences = ["can you get the ", "the ", "da ","that is a ","that's a ","and the ","a ","it is a ","this is a ","and a ","can you say ","here is the ","and ","where is the ","that is the ","look at the ","i have the ","you want the ","color is the ","is that the ","there is the ","you put the ","to put the ","one is the "]
    for matchSentence in matchSentences:
        matchResults = re.findall(' ' +matchSentence + '[a-z]+',sentence) #find word groups that are: sample sentence + word
        for match in matchResults:
            match = match.replace(' ' + matchSentence,'') #remove sample sentence
            if obj != "": # if it's not the firsh object found
                if len(re.findall(match,obj)) == 0: # if the object has not already been found
                    obj = obj + " "
                    obj = obj + match 
            else :
                obj = obj + match 
    return obj

def get_obj_by_POS_and_sentences(sentence):
    """
        take a str and retrun a list of objects, 
        the list is the intersection of strategy 
        1- obj found by typical sentences
        2- nouns found by POS tagging
    """
    list_obj1 = getObj(sentence) 
    list_obj2 = getNouns(sentence)
    list_obj1 = list_obj1.split(" ")
    list_obj2 = list_obj2.split(" ")
    return list(set(list_obj1).intersection(list_obj2))



def getTextFromCha(filePath):
    """
        take cha file return a str with only speech cleaned
    """
    lines = getSpeechLines(filePath)  #tab with speech lines only
    txt = ""
    for line in lines: 
        if txt != "":
            txt = txt + ". "
        splittedLine = splitOneLine(line)
        if len (splittedLine) >0:# if the splitted line is not empty --> the speech is not empty
            txt = txt + splittedLine[0][3]
    txt = txt.replace(" .",".")
    txt = re.sub("\.+",".", txt)
    return (txt) 
    


def main():
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", help=".cha file folder path")
    args = vars(ap.parse_args())
    if args.get("input", None) is not None:
        # read arguments
        chaFolderPath = args["input"]
        for filename in os.listdir(chaFolderPath):
            """
                Browe all the cha files, for each files in the folder check 
                if it's a cha file and if it's a Rollins cha file like 
                if true : find objects in speech and write it in a .txt file
            """
            match = re.match("[a-z][a-z][0-9][0-9]\.cha",filename)
            if match:
                if chaFolderPath[-1] != "/":
                    writeFileWithAllObject(chaFolderPath + "/" + filename)
                else:
                    writeFileWithAllObject(chaFolderPath + filename)

if __name__ == "__main__":
    main()
    
    
    
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

def add_obj_POS_sentence(line):
    obj = get_obj_by_POS_and_sentences(line[3])
    str_obj = ""
    for elt in obj:
        if str_obj != "":
            str_obj += " "
        str_obj += elt
    line.append(str_obj)
    return line
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
    return off

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
        cat = "Sample sentences "
    
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

def saveInFile(filePath):
    lines = getSpeechLines(filePath)
    print (lines)
    contentTab = splitLines(lines)
    filename = getFileName(filePath)
    file = open("DATA/" + filename + '.txt','w')
    file.write('name,on,off,sentence,Objects\n')
    #print ("len de contentTab" + str(len(contentTab)))
    for content in contentTab:
        content = add_obj_POS_sentence(content)
        content = tabToString(content)
        file.write(content)
        
