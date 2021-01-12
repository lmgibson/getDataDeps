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
            if entry.endswith(".R"):
                allRFiles.append(fullPath)

    return allRFiles


allRFiles = getListOfFiles(".")

data = {}
saveData = []
readData = []
for file in allRFiles:
    data[file] = {}

    save = os.popen(
        'cat ' + file + ' | grep -A 1 "saveRDS*" | grep -o \'".*"\' | sed \'s/"//g\'').read()
    read = os.popen(
        'cat ' + file + ' | grep -A 1 "readRDS*" | grep -o \'".*"\' | sed \'s/"//g\'').read()

    save = save.splitlines()
    read = read.splitlines()

    if len(save) > 0:
        saveData.extend(save)
    if len(read) > 0:
        readData.extend(read)

    data[file]['save'] = save
    data[file]['read'] = read

print("Saved datasets:")
[print("\t", x) for x in saveData]

print("Read datasets:")
[print("\t", x) for x in readData]

print("Datasets that are saved and not read:")
[print("\t", x) for x in (set(saveData) - set(readData))]
