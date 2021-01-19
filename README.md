# Overview
getDataDeps is a script that maps data dependencies across R and python files in your project.
The tool currently tracks data dependencies in R, but can be easily extended to track files in python scripts.

# Use
The code can be ran by using `python ./getDataDeps.py` if the code is located in the root of your project.
Always run the script from the root of your project. If you save the getDataDeps.py script in another location
you can call it using `python [path to script]/getDataDeps.py`

# How it works
The script will iterate through your entire project folder, extract files that end in ".R" or ".py",
and then collect information on data imports and data exports. The json object will be saved to
in the 'dataDepsOutput' folder as 'dataDeps.json' and the graph as 'dataDepsGraph.svg'.

Below is a very simple graph to give you a rough idea of the ouput.

![](./dataDepsOutput/dataDepsGraph.png)
