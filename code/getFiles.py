import os
import sys


def getDirectoryToMap():
    """
    If a directory is given the script willstick to that directory. Otherwise
    it will search the directory in which the script is initialized.
    Returns string variable.
    """
    if len(sys.argv) > 1:
        dirToSearch = sys.argv[1]
    else:
        dirToSearch = "."

    return dirToSearch


def getListOfFiles(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allCodeFiles = list()

    # blacklisted directory names
    ignoreDirectoriesContaining = [
        'conda-env', 'archive', 'old', 'getDataDeps']

    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)

        # If entry is a directory then get the list of files in this directory
        # if it isn't a directory, and ends with .R  or .py and the fullpath doesn't contain
        # a blacklisted string, then append it to list of R files.
        if os.path.isdir(fullPath):
            allCodeFiles = allCodeFiles + getListOfFiles(fullPath)
        else:
            if (entry.endswith(".R") or entry.endswith(".py") or entry.endswith(".do")) and (not any([x in fullPath for x in ignoreDirectoriesContaining])):
                allCodeFiles.append(fullPath)

    # Fixes paths if this is run on windows, has no impact on macs
    allCodeFiles = [x.replace('\\', '/') for x in allCodeFiles]
    return allCodeFiles
