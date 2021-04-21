import json
import pydot
import os
import sys


def getDirectoryToMap():
    """
    If a directory is given the script willstick to that directory. Otherwise
    it will search the directory in which the script is initialized.

    Returns:
        str : string indicating the path to the directory to search
    """
    if len(sys.argv) > 1:
        dirToSearch = sys.argv[1]
    else:
        dirToSearch = "."

    return dirToSearch


def getListOfFiles(dirName):
    """
    Given a directory path finds all .R, .py, and .do files
    within that directory. Returns files and their paths (relative
    to the specified directory) in a list

    Args:
        dirName (str): Path of directory to search

    Returns:
        list: List of relative file paths for .R, .py, and .do files
    """
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    listOfCodeFiles = list()

    # blacklisted directory names
    ignoreDirectoriesContaining = [
        'conda-env', 'archive', 'old', 'getDataDeps']

    # Iterate over all the entries
    for file in listOfFile:
        # Create relative path from given directory
        fullPath = os.path.join(dirName, file)

        # If entry is a directory then get the list of files in this directory
        # if it isn't a directory, and ends with .R  or .py and the fullpath doesn't contain
        # a blacklisted string, then append it to list of R files.
        if os.path.isdir(fullPath):
            listOfCodeFiles = listOfCodeFiles + getListOfFiles(fullPath)
        else:
            if (file.endswith(".R") or file.endswith(".py") or file.endswith(".do")) and (not any([x in fullPath for x in ignoreDirectoriesContaining])):
                listOfCodeFiles.append(fullPath)

    # Fix paths if run on windows Unix emulator, has no impact on macs
    listOfCodeFiles = [x.replace('\\', '/') for x in listOfCodeFiles]

    return listOfCodeFiles


def extractPyOrRFiles(file):
    """
    Uses Unix commands to search for and extract datasets from R
    or Python files.

    Args:
        file (str): Path to a .R or .Py file

    Returns:
        list: A list of strings containing the datasets saved and read
    """
    save = os.popen(
        'cat ' + file + ' | grep -A 1 "saveRDS*\|write[_.]csv*\|to_csv*" | grep -o \'".*"\' | sed \'s/"//g\' ').read()
    read = os.popen(
        'cat ' + file + ' | grep -A 1 "readRDS*\|read_csv*" | grep -o \'".*"\' | sed \'s/"//g\' ').read()

    return save, read


def extractDoFiles(file):
    """
    EXPERIMENTAL
    Uses Unix commands to search for and extract datasets from do files.

    Args:
        file (str): Path to a .R or .Py file

    Returns:
        list: A list of strings containing the datasets saved and read
    """
    # Grepping commands
    # foreachVars = os.popen(
    #     'cat ' + file + ' | awk \'{$1=$1;print}\' | grep "^foreach .* in" | awk \'{for(i=2;i<NF;i++)print $(i)}\' | sed \'s/in//g\' | tr \'\n\' \',\' | sed \'s/,,/,/g\' ').read()
    localVars = os.popen(
        'cat ' + file + ' | grep "^local" | awk \'{print $2,$3}\' | sed \'s/ /,/g\' ').read()
    save = os.popen(
        'cat ' + file + ' | grep "^save" | awk \'{print $2}\' | sed \'s/,//g\' | sed \'s/\"//g\' ').read()
    read_import = os.popen(
        'cat ' + file + ' | grep "^import" | awk \'{print $3}\' | sed \'s/,//g\' | sed \'s/\"//g\' ').read()
    read_use = os.popen(
        'cat ' + file + ' | grep "^use" | awk \'{print $2}\' | sed \'s/,//g\' | sed \'s/\"//g\' ').read()
    read_merge = os.popen(
        'cat ' + file + ' | awk \'{$1=$1;print}\' | grep "^merge" | awk \'{for(i=1;i<=NF;i++)if($i=="using")print $(i+1)}\' | sed \'s/\"//g\' ').read()
    read_append = os.popen(
        'cat ' + file + ' | awk \'{$1=$1;print}\' | grep "^append" | awk \'{for(i=1;i<=NF;i++)if($i=="using")print $(i+1)}\' | sed \'s/\"//g\' ').read()
    read = read_import + read_use + read_merge + read_append

    # Converting local var into dictionary.
    localVarDict = {}
    for i in [x.split(',') for x in localVars.splitlines()]:
        if len(i) > 0:
            localVarDict[('`' + i[0] + '\'')] = i[1]

    # Replacing values matching keys in local vars with the
    # keys value. Assumes local vars are constant through script.
    for j in localVarDict:
        save = save.replace(j, localVarDict[j])
        read = read.replace(j, localVarDict[j])

    # Removing the temp file tags `xxx'
    save = save.replace('`', '').replace('\'', '')
    read = read.replace('`', '').replace('\'', '')

    return save, read


def cleanFilePaths(listOfResults, type=None):
    if type not in ['save', 'read']:
        raise ValueError(
            "Please specify whether or not listOfResults is"
            "'save' or 'read' list.")

    if not isinstance(listOfResults, list):
        raise ValueError(
            "Please provide a list to 'listOfResults'"
        )

    for dataFile in listOfResults:
        dataFile = dataFile.rsplit('/', 1)[-1]
        if dataFile not in data:
            data[dataFile] = {'save': [], 'read': []}
            data[dataFile][type].append(listOfResults.rsplit('/', 1)[-1])
        else:
            data[dataFile][type].append(listOfResults.rsplit('/', 1)[-1])


def extractDataDeps(listOfCodeFiles):
    data = {}
    saveData = []
    readData = []

    for file in listOfCodeFiles:
        print(file)
        # Cat reads out contents of found script, first grep finds all lines with import / export commands,
        # second grep finds things stuck between double quotes, third grep removes the quotes
        if any(fileEnding in file for fileEnding in ['.R', '.py']):
            save, read = extractPyOrRFiles(file)
        elif '.do' in file:
            save, read = extractDoFiles(file)
        else:
            sys.exit(
                "Something went wrong. The 'getListOfFiles' function saved a file that doesn't end in .do, .R, or .py")

        save = save.splitlines()
        read = read.splitlines()

        for dataFile in save:
            dataFile = dataFile.rsplit('/', 1)[-1]
            if dataFile not in data:
                data[dataFile] = {'save': [], 'read': []}
                data[dataFile]['save'].append(file.rsplit('/', 1)[-1])
            else:
                data[dataFile]['save'].append(file.rsplit('/', 1)[-1])

        for dataFile in read:
            dataFile = dataFile.rsplit('/', 1)[-1]
            if dataFile not in data:
                data[dataFile] = {'save': [], 'read': []}
                data[dataFile]['read'].append(file.rsplit('/', 1)[-1])
            else:
                data[dataFile]['read'].append(file.rsplit('/', 1)[-1])

        if len(save) > 0:
            saveData.extend(save)
        if len(read) > 0:
            readData.extend(read)

    return data, saveData, readData


def createDepGraph(data):
    dot_graph = pydot.Dot(graph_type='digraph')

    for i, val in enumerate(data):
        # Add node for the dataset
        node = pydot.Node(val)
        node.set_shape('box2d')
        dot_graph.add_node(node)

        # Add nodes above the dataset for the file(s) that create it
        # Add an edge from the file to the dataset
        for j in data[val]['save']:
            node = pydot.Node(j)
            node.set_shape('box2d')
            dot_graph.add_node(node)

            edge = pydot.Edge(j, val)
            dot_graph.add_edge(edge)

        # Add edges from the dataset to the files it is read by
        if data[val]['read']:
            for j in data[val]['read']:
                edge = pydot.Edge(val, j)
                dot_graph.add_edge(edge)

    return dot_graph


def outputResults():
    print("Saved datasets:")
    [print("\t", dataFile) for dataFile in set(saveData)]

    print("Read datasets:")
    [print("\t", dataFile) for dataFile in set(readData)]

    print("Datasets that are saved and not read:")
    [print("\t", dataFile) for dataFile in (set(saveData) - set(readData))]

    print("\nFor detailed information see the dataDeps.json file.")
    with open('./dataDepsOutput/dataDeps.json', 'w') as outfile:
        json.dump(data, outfile)

    print("\nA graph of your data dependencies is available as './dataDepsOutput/dataDepsGraph.png'")


if __name__ == '__main__':
    # Note, if you drop this into a function it greys out saveData and readData. Not sure why.
    # Get dir to search, if given
    dirToSearch = getDirectoryToMap()

    # Recursively obtain list of R files
    listOfCodeFiles = getListOfFiles(dirToSearch)

    # Extract dependencies from R files
    data, saveData, readData = extractDataDeps(listOfCodeFiles)

    # Create dependency graph
    graph = createDepGraph(data)

    # Write graph to output folder
    if not os.path.exists('./dataDepsOutput'):
        os.makedirs('./dataDepsOutput')
    graph.write_png('./dataDepsOutput/dataDepsGraph.png')

    # Print results and write data to json object
    outputResults()
