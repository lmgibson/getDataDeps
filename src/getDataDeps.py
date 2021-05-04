import json
import pydot
import os
import sys
from rich.console import Console


def getDirectoryToMap():
    """
    If a directory is given the script willstick to that directory. Otherwise
    it will search the directory in which the script is initialized.

    Returns:
        str : string indicating the path to the directory to search
    """
    if len(sys.argv) > 1:
        projectFolder = sys.argv[1]
        if projectFolder[-1] == "/":
            dirToSearch = projectFolder
        else:
            dirToSearch = projectFolder + "/"
    else:
        dirToSearch = "./"

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


def cleanFilePaths(file, listOfResults, type=None):
    """
    Constructs the data which consists of a dictionary within a dictionary.
    The first level has keys that are the data file name, and the second
    level contains two keys: saved and read. Within 'saved' and 'read'
    are a list that contains the scripts that either save or read
    the data file.

    Args:
        file (str): Path to a script that is being scanned
        listOfResults (list): List of strings of data files used in file
        type (string, optional): String to indicate if the list supplied
        contains saved datafiles or read data files. Defaults to None.

    Returns:
        dict : Dictionary of format described above
    """
    if type not in ['save', 'read']:
        raise ValueError(
            "Please specify whether or not listOfResults is"
            "'save' or 'read' list.")

    if not isinstance(listOfResults, list):
        raise ValueError(
            "Please provide a list to 'listOfResults'"
        )

    results = {}

    for dataFile in listOfResults:
        dataFile = dataFile.rsplit('/', 1)[-1]
        if dataFile not in results:
            results[dataFile] = {'save': [], 'read': []}
            results[dataFile][type].append(file.rsplit('/', 1)[-1])
        else:
            results[dataFile][type].append(file.rsplit('/', 1)[-1])

    return results


def extractDataDeps(listOfCodeFiles):
    """
    The meat. Takes in a list of files, examines relevant files for datafiles
    saved or read, and exports the results in a dictionary labeled 'data'.

    Args:
        listOfCodeFiles (list): List of strings where each string is a file in
        the supplied directory.

    Returns:
        dict: Returns three dictionaries that contain a top-level dictionary
        where the key is the data file, a sub-level dictionary where the key
        is 'saved' or 'read' and within each of those keys a list of strings
        of the files that use the top-level key.
    """
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

        data.update(cleanFilePaths(file, save, type='save'))
        data.update(cleanFilePaths(file, read, type='read'))

        if len(save) > 0:
            saveData.extend(save)
        if len(read) > 0:
            readData.extend(read)

    return data, saveData, readData


def createDepGraph(data):
    """
    Constructs a graph connecting data files to scripts using the multi-level
    dictionary object.

    Args:
        data (dictionary): Multi-level dictionary connecting data files to 
        scripts that save and read them.

    Returns:
        graph: A pydot graph object
    """
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


def saveGraph(graph, dirToSearch):
    """
    Constructs directory for graph if it doesn't exist. Saves graph.

    Args:
        graph (graph): Pydot graph object.
    """
    if not os.path.exists('%sdataDepsOutput' % (dirToSearch)):
        os.makedirs('%sdataDepsOutput' % (dirToSearch))

    try:
        graph.write_png('%sdataDepsOutput/dataDepsGraph.png' % (dirToSearch))
    except:
        print("Saving out the graph failed. You most likely need to install graphviz.")


def writeData(data, dirToSearch):
    """
    Saves data dictionary out as a json object.

    Args:
        data (dict): Dictionary mapping data files to the
        scripts that save and read them.
    """
    fileName = '%sdataDepsOutput/dataDeps.json' % (dirToSearch)

    with open(fileName, 'w') as outfile:
        json.dump(data, outfile)


def printResults(dirToSearch, saveData, readData, console):
    """
    Prints results to console.
    """
    console.print("\n[bold]Saved datasets[/bold]:\n")
    [console.print("\t", dataFile) for dataFile in set(saveData)]

    console.print("\n[bold]Read datasets[/bold]:\n")
    [console.print("\t", dataFile) for dataFile in set(readData)]

    console.print("[bold]Datasets that are saved and not read[/bold]:")
    [console.print("\t", dataFile)
     for dataFile in (set(saveData) - set(readData))]

    console.print("\nFor detailed information see the dataDeps.json file.")

    console.print(
        "\nA graph of your data dependencies is available as '%sdataDepsOutput/dataDepsGraph.png'" % (dirToSearch))


def main():
    console = Console()

    # Get dir to search, if given
    dirToSearch = getDirectoryToMap()

    # Recursively obtain list of files
    listOfCodeFiles = getListOfFiles(dirToSearch)

    # Extract dependencies from files
    data, saveData, readData = extractDataDeps(listOfCodeFiles)

    # Create dependency graph
    graph = createDepGraph(data)

    # Write graph to output folder
    saveGraph(graph, dirToSearch)

    # Write Data to output folder
    writeData(data, dirToSearch)

    # Print results and write data to json object
    printResults(dirToSearch, saveData, readData, console)


if __name__ == '__main__':
    main()
