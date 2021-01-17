import json
import pydot
import os


def getListOfFiles(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allCodeFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allCodeFiles = allCodeFiles + getListOfFiles(fullPath)
        else:
            if entry.endswith(".R"):
                allCodeFiles.append(fullPath)

    return allCodeFiles


def extractDataDeps(allCodeFiles):
    data = {}
    saveData = []
    readData = []

    for file in allCodeFiles:
        save = os.popen(
            'cat ' + file + ' | grep -A 1 "saveRDS*" | grep -o \'".*"\' | sed \'s/"//g\'').read()
        read = os.popen(
            'cat ' + file + ' | grep -A 1 "readRDS*" | grep -o \'".*"\' | sed \'s/"//g\'').read()

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


def outputResults():
    print("Saved datasets:")
    [print("\t", dataFile) for dataFile in set(saveData)]

    print("Read datasets:")
    [print("\t", dataFile) for dataFile in set(readData)]

    print("Datasets that are saved and not read:")
    [print("\t", dataFile) for dataFile in (set(saveData) - set(readData))]

    print("\nFor detailed information see the dataDeps.json file.")
    with open('./dataDeps.json', 'w') as outfile:
        json.dump(data, outfile)

    print("\nA graph of your data dependencies is available as 'dataDepsGraph.png'")


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


# Putting it together
allRFiles = getListOfFiles(".")
data, saveData, readData = extractDataDeps(allRFiles)
graph = createDepGraph(data)
graph.write_png('./dataDepsGraph.png')
outputResults()
