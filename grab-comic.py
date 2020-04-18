# MIT License
# Copyright (C) Alexander Radkov 2020

import codecs
import re
import requests
import shutil

from os import listdir, mkdir
from os.path import isfile, join, exists

# Get all files in the ./Pages directory
srcDir = 'Pages'
dstDir = 'Comic'
allFiles = [f for f in listdir(srcDir) if isfile(join(srcDir, f))]

if not exists(dstDir):
    mkdir(dstDir)

for f in allFiles:
    comicTitle = "Unknown"
    comicIssue = 0
    searchObj = re.search( r'Issue #(\d)+', f, re.M|re.I)
    if searchObj:
        comicIssue = int(re.sub(r'\D', "", searchObj.group(0)))
        titleLines = f.split(searchObj.group(0))
        comicTitle = titleLines[0].strip()
    print("***************************")
    print('Title: ({})'.format(comicTitle))
    print('Issue: ({:02d})'.format(comicIssue))
    
    destinationFolder = join(join(dstDir, comicTitle), 'Issue {:02d}'.format(comicIssue))
    if not exists(join(dstDir, comicTitle)):
        mkdir(join(dstDir, comicTitle))
    if not exists(destinationFolder):
        mkdir(destinationFolder)
    print('Saving to ({})'.format(destinationFolder))
    print("Downloading ... ", end = '')
    
    htmlFile = codecs.open(join(srcDir, f) , "r", "utf-8")
    htmlText = htmlFile.read()
    # Get all lines containing the image url:
    matched_lines = [line for line in htmlText.split('\n') if "lstImages.push" in line]
    pageNumber = 1
    for l in matched_lines:
        imgUrl = l.replace('lstImages.push("','').replace('");','').strip()
        saveImgFile = '{} Issue {:02d} - {:03d}.jpg'.format(comicTitle, comicIssue, pageNumber)
        
        if not isfile(join(destinationFolder, saveImgFile)):
            local_file = open(join(destinationFolder, saveImgFile), 'wb')
            resp = requests.get(imgUrl, stream=True)
            resp.raw.decode_content = True
            shutil.copyfileobj(resp.raw, local_file)
            del resp
            print('{:02d} '.format(pageNumber), end = '')
        pageNumber += 1
    print('done')
    print("***************************")

print("***************************")
print('HAPPY READING!!!11!1!!111')
print("***************************")
