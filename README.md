getDataDeps-R is a command line tool that maps data dependencies across R files in your project.
The tool is currently a work in progress but when it is complete it will return a list of datasets saved and read,
a json object, and a graph built from the json object.

If the code is in the root of your project, it can be run by:
`python getDataDeps.py`

Which will iterate through your entire project folder, extract files that end in ".R", and then collect information
on data imports and data exports. The json object will be saved to the root as 'dataDeps.json' and the graph as 'dataDepsGraph.svg'.
