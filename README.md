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

# Helpful tips

For best results limit your import and export data commands to two-lines. The script looks for the import/export commands and then looks a maximum of one line below it. Furthermore, it would be best to maintain at least one line between import/export commands and the code below it. Because the script is looking one line below where it finds the import/export command it will include any line below a single line import/export command. This can be problematic if you save out your data and immediate print something on the following line.
