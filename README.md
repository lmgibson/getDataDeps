# Overview
getDataDeps-R is a script that maps data dependencies across R files in your project.
The tool is currently a work in progress but when it is complete it will return a list of datasets
saved and read, a json object, and a graph built from the json object.

# Use
The code can be ran by using `python ./getDataDeps.py` if the code is located in the root of your project.
If you save the code in another location just call it based on that location.

# How it works
The script will iterate through your entire project folder, extract files that end in ".R",
and then collect information on data imports and data exports. The json object will be saved to
in the 'dataDepsOutput' folder as 'dataDeps.json' and the graph as 'dataDepsGraph.svg'.
