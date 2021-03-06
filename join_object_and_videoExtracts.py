#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 01:24:23 2018

@author: lea
"""

import os
import re
import argparse

def getMainVideoName(txtFilePath):
    """
        takes a video extract filename (str) and return the main video name (str)
    """
    videoName = txtFilePath.split('/')[-1]
    videoName = videoName.split('.')[0]
    return videoName

def get_on_off_videoExtract(filename):
    """
        takes a video file name and extracts the beginning and 
        end of the video in a table
    """
    duration = []
    filename = filename.replace('.mp4','')
    filename = filename.split('_')
    duration.append(filename[1])
    duration.append(filename[2])    
    return duration

def get_on_off_txtFileLine(line):
    """
        takes a line of txt (str) and retun a tab with speechStart and speehStop
    """
    duration = []
    line = line.split(',')
    duration.append(line[1])
    duration.append(line[2])
    return duration


def browseVideoFiles(text_file, video_folder, videoOnlinePath):
    """
        input :  
            text_file (str) text file path 
            video_folder :  path to all video extracts
            videoOnlinePath : Prefix that will allow the video to be accessible online
            
        from the name of a text file, we find all the associated videos 
        and we look for the names of objects that are said during the video 
        in the lines of the text file
        return noting but edit or create a csv file with video path and objects names
    """
    csvfile = open ("/DATA/videoAndObjects.csv",'w')
    videoName = getMainVideoName(text_file)
    for filename in os.listdir(video_folder):
        #videoPath = video_folder + '/' + filename
        match  = re.match(videoName + '.+.mp4', filename)
        if match:
            video_duration = get_on_off_videoExtract(filename)
            video_start = float(video_duration[0])
            video_end = float(video_duration[1])
            text_content = open(text_file,'r')
            objList = "" # Don't write directly the objects names to not have the same object name twice
            for line in text_content:
                speech_duration = get_on_off_txtFileLine(line)
                if speech_duration[0] != 'on':
                    speech_start = float(speech_duration[0]) * 0.001
                    speech_end = float(speech_duration[1]) * 0.001
                    # If speech or part of speech occurs during the video
                    if (speech_start < video_end and speech_start > video_start) or (speech_end < video_end and speech_end > video_start) or (speech_start < video_start and speech_end > video_end):
                        obj = line.split(',')[4]
                        obj = obj.replace('\n','')
                        if obj != "":
                            if objList != "":
                                test = obj.split(' ')
                                for elt in test:
                                    if elt not in objList:
                                        objList += ";"
                                        objList += elt
                            else: 
                                obj = obj.replace(' ',';')
                                objList += obj
            csvfile.write(videoOnlinePath + filename + ',' + objList+'\n')
            
            
def createCSVFile(textFolderPath, videoFolderPath, onlinePath):
    """
        Input :
            textFolderPath : folder that contains text files that contain 
            speech and objects extracted from speech.
            videoFolderPath : folder that contains the video extracts. 
            The names of the video extracts contains their start and end times.
            onlinePath : Prefix that will allow the video to be accessible online
        
        browse txt files with objects names and speech duration
    """
    for filename in os.listdir(textFolderPath):
        match = re.match("[a-z][a-z][0-9][0-9]\.txt", filename)
        if match:
            if textFolderPath[-1] != "/":
                browseVideoFiles(textFolderPath + "/"+ filename, videoFolderPath, onlinePath)
            else:
                browseVideoFiles(textFolderPath + filename, videoFolderPath, onlinePath)
        

def main():
    """
        create a csv file with video names and objects presents in the video(separated by ';')
        You can specify the online prefix link to the video, and directly use the csv for AMT task2
    """
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--text", help="Text(s) folder path with objects and names")
    ap.add_argument("-v", "--video", help="Videos extracts folder path")
    ap.add_argument("-p","--path",type=str,default="", help="video path when the video will be online (default none)")
    args = vars(ap.parse_args())
    
    # read arguments
    videoFolderPath = args["video"]
    textFolderPath = args["text"]
    
    if args.get("text", None) is None:
        print ("a text folder path is required")
    elif args.get("video", None) is None:
        print ("a video folder path is required")
    elif args.get("path", None) is not None:
        onlinePath = args["path"]
        createCSVFile(textFolderPath, videoFolderPath, onlinePath)
    else: 
        createCSVFile(textFolderPath, videoFolderPath, "")
    
    


if __name__ == "__main__":
    main()

               
        


