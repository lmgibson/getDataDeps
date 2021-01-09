import json
import os


def getListOfFiles(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allRFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allRFiles = allRFiles + getListOfFiles(fullPath)
        else:
            if ".R" in fullPath:
                allRFiles.append(fullPath)

    return allRFiles


allRFiles = getListOfFiles(".")

data = {}
for file in allRFiles:
    data[file] = {}
    save = os.popen(
        'cat ' + file + ' | grep "save*" | grep -o \'".*"\' | sed \'s/"//g\'').read()
    read = os.popen(
        'cat ' + file + ' | grep "read*" | grep -o \'".*"\' | sed \'s/"//g\'').read()

    save = save.splitlines()
    read = read.splitlines()

    data[file]['save'] = save
    data[file]['read'] = read

print(json.dumps(data))
