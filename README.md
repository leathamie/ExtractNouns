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

ex of input
ex of output

clean cha and extract sentences --> search objects names in all file --> POS tagging U sample sentence --> get an all file obj list --> browse lines and for each associate objects.
Why not by beginning? Because we whant to be assured that we catch all occurrences.

- dans le nettoyage on a laissé les ' pour le POS tagging 
- on a rajouté des phrases types en transformant les existantes en orales "the" = "da"

- cas ou il n'y a pas les durées 
AMméliorations à faire : 
-colors

## join_object_and_videoExtracts.py
ex input
output
fonctionnement général 

