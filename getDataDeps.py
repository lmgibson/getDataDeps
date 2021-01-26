import json
import pydot
import os


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
            if (entry.endswith(".R") or entry.endswith(".py")) and (not any([x in fullPath for x in ignoreDirectoriesContaining])):
                allCodeFiles.append(fullPath)

    return allCodeFiles


def extractDataDeps(allCodeFiles):
    data = {}
    saveData = []
    readData = []

    for file in allCodeFiles:
        save = os.popen(
            'cat ' + file + ' | grep -A 1 "saveRDS*\|write[_.]csv*\|to_csv*" | grep -o \'".*"\' | sed \'s/"//g\'').read()
        read = os.popen(
            'cat ' + file + ' | grep -A 1 "readRDS*\|read_csv*" | grep -o \'".*"\' | sed \'s/"//g\'').read()

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


# Recursively obtain list of R files
allCodeFiles = getListOfFiles(".")

# Extract dependencies from R files
data, saveData, readData = extractDataDeps(allCodeFiles)

# Create dependency graph
graph = createDepGraph(data)

# Write graph to output folder
if not os.path.exists('./dataDepsOutput'):
    os.makedirs('./dataDepsOutput')
graph.write_png('./dataDepsOutput/dataDepsGraph.png')

# Print results and write data to json object
outputResults()
