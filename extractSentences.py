#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 16 07:59:39 2018

@author: lea
"""

import re

def extractFileContent(filename):
    fileContent = ""
    file = open(filename, "r")
    for line in file : 
        fileContent = fileContent + line
    return fileContent


def getSpeechLines(filePath):
    content = extractFileContent(filePath)
    line_tab = re.findall('\*MOT:.*_[0123456789][0123456789]*', content)
    print (len(line_tab))
    return line_tab

def splitLines(speechLines):
    lines = []
    for line in speechLines:
        splitLine = splitOneLine(line)
        lines.append(splitLine)
    return lines

def splitOneLine(line):
    print (line)
    line = line.split(':\t')
    act = line[0]
    act = act.replace('*','')
    print(act)
    line = line[1]
    line = line.split('\x15')
    sentence = line[0]
    line = line[1]
    line = line.split('_')
    on = line[0]
    off = line[1]
    print ("sentence "+sentence)
    print ("on " + on)
    print ("off "+ off)
    return act + ',' +  on + ',' + off + ',' + sentence + '\n'

def getFileName(filePath):
    filename = filePath.split('/')[-1]
    if len(filename) == 0 :
        filename =filePath.split('.')[0]
    else : 
        filename = filename.split('.')[0]
    return filename
    
def saveInFile(filePath):
        lines = getSpeechLines(filePath)
        contentTab = splitLines(lines)
        filename = getFileName(filePath)
        file = open(filename + '.txt','w')
        file.write('name,on,off,sentence\n')
        for content in contentTab:
            file.write(content)
        
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


