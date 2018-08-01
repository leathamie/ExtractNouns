# Exract objects names from  for AMT task2
The purpose of both scripts is to have the list of objects present in each video clip from the video transcripts. So we have a.cha file folder that contains video transcriptions and a video clips folder that comes from the repo: https://github.com/leathamie/ExtractVideo
In the output of the two scripts (in the order extract_objectsNames_in_txtFiles.py then join_object_and_videoExtracts.py) we have a.csv file usable on Amazon Mechanical Turk (see :https://github.com/bootphon/ActionsTagging) this file will contain in the first line the list of video extracts and in the second column the objects extracted from the associated speech.

## Prerequisites
These scripts run from the command line, they use python 3 and nltk 3.3 on ubuntu 16.04.
## extract_objectsNames_in_txtFiles.py
this script takes in.cha files that contain transcripts and outputs text files of the following form :

```
MOT,1038518,1040650,good push ,
MOT,1046481,1056481,in the box ,box
MOT,1056481,1058345,yay ,
MOT,1058345,1060671,out of the box ,box
MOT,1063081,1064436,where you going ,
MOT,1067630,1068940,did you find another chair ,chair
MOT,1078510,1080155,you could stand up and walk over there ,walk
MOT,1080155,1080961,come here ,
MOT,1080961,1082910,come here ,
MOT,1082910,1084611,nope ,
MOT,1084611,1093208,stand up ,
MOT,1093208,1106451,do you like playing with the chairs ,chair chairs
MOT,1106451,1109888,do you want bird to sit in the chair ,chair
```
In the first column there is the speaker (in this version only the mother's speech has been retrieved), in the second column there is the speech start time in milliseconds, in the 3rd column there is the speech end time in milliseconds, in the 4th column there is the speech and in the last column the found objects.

Overall the program cleans the.cha file to extract only the mother's speech. Then it performs a POS tagging and a word search based on phrases on this text. So we get 2 list of words, we keep the words that are present in both lists.  Then we create a file where we will write the sentences said, when they were said and what words from the list are present.

We took the example of the article"""" and we have this list of sentences`:
```
"can you get the ", "the ", "da ","that is a ","that's a ","and the ","a ","it is a ","this is a ","and a ","can you say ","here is the ","and ","where is the ","that is the ","look at the ","i have the ","you want the ","color is the ","is that the ","there is the ","you put the ","to put the ","one is the "
```
if a word is preceded by one of these sentences he is probably an object. Wee add some verbal equivalent sentences, for example if 'the' is present we add 'da'

This script only takes as argument the cha folder path. You can lunch the scprit il command line with for example:
'''
python extract_objectsNames_in_txtFiles.py -i '/chaFolderpath'
'''

When we clean the .chat file we remove all punctuation or special characters, we leave the apostrophes because the NLTK POS tagging works very badly without.

If the lyrics durations are not specified in the .cha then no phrase will be selected and it is possible to have a file that will be created but will be empty.

### improvements to be made :
- do not create a file when there is no sentence with a duration
- add a possible color list in sentences

## join_object_and_videoExtracts.py
this script takes in parameter two folders, the one with all the text files created by the previous script and a folder with all the video clips. Video clips are named in a particular way : MainVideoName_Start_Stop.mp4 start and stop are in seconds.
ex input
```
 python join_object_and_videoExtracts.py -t'textFolderPath' -v'videoClipFolderPath'
```
You can also specify a path for the online video, it will be add before the 
output
fonctionnement général 

