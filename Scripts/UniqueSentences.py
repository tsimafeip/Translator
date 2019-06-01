# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 21:43:41 2019

@author: Tima
"""

#Backup files contain unique sentences from all alingned chunks
fileBackupRus = r'd:\Data\BackupRus.txt'
fileBackupBel = r'd:\Data\BackupBel.txt'

#Index determines current aligned chunk
index = 5
alignedFileBel = r'd:\Data\AlignedData\BelarusssianAligned{}.txt'.format(index)
alignedFileRus = r'd:\Data\AlignedData\RusssianAligned{}.txt'.format(index)

logsRus = r'd:\Data\LogsRus.txt'
logsBel = r'd:\Data\LogsBel.txt'

with open(fileBackupRus, 'r', encoding = "utf-8") as fileRusToRead, open (fileBackupBel, 'r', encoding = "utf-8") as fileBelToRead:
    listRus = fileRusToRead.readlines()
    listBel = fileBelToRead.readlines()

with open(fileBackupRus, 'a', encoding = "utf-8") as fileRus, open (fileBackupBel, 'a', encoding = "utf-8") as fileBel, open (logsRus, 'a', encoding = "utf-8") as logsFileRus, open (logsBel, 'a', encoding = "utf-8") as logsFileBel:
    currentLineNum = 1
    for (lineBel, lineRus) in zip(open(alignedFileBel, 'r', encoding = "utf-8"), open(alignedFileRus, 'r', encoding = "utf-8")):
        if lineRus in listRus or lineBel in listBel:
            print("Found bel/rus")
            logsFileBel.write("Bel{}({}): {}".format(index, currentLineNum, lineBel))
            logsFileRus.write("Rus{}({}): {}".format(index, currentLineNum, lineRus))
        else:
            listRus.append(lineRus)
            listBel.append(lineBel)
            fileRus.write(lineRus)
            fileBel.write(lineBel)
        currentLineNum+=1

