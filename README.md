[![Build Status](https://www.travis-ci.com/lmgibson/getDataDeps.svg?branch=main)](https://www.travis-ci.com/lmgibson/getDataDeps)

# Overview

getDataDeps is a script that maps data dependencies across R and python files in your project. The tool currently tracks data dependencies for several import/export commands in R, python, and Stata.

# Getting Started

Make sure pydot is installed. You can install it using either `conda install pydot` or `pip install pydot`. Next, download the script (getDataDeps.py) to your computer. Now you can map a project by navigating to the root of the project directory `cd ~/Desktop/project/statisticsAndStuff` and then running `python path/to/script/getDataDeps.py`. The prior command will map the entire project directory. If you want to map a subdirectory you can specify it as `python path/to/script/getDataDeps.py ./code`.

If successful, the script will return output to the terminal as well as two files located in dataDepsOutput within the root of your project directory.

# How it works

The script will iterate through your entire project folder, extract files that end in “.R”, “.py", or ".do", and collect information on data imports and data exports. The JSON object will be saved in the ‘dataDepsOutput’ folder as ‘dataDeps.json’ and the graph as ‘dataDepsGraph.png.

The script will search the entire directory in which it is called. However, you can specify a directory as an option. Here's an example that will run the script on a directory titled 'code':
`python path/to/script/getDataDeps.py ./code`

Below is a very simple graph to give you a rough idea of the ouput.

![](./dataDepsOutput/dataDepsGraph.png)

# Helpful tips

For best results limit your import and export data commands to two-lines. The script looks for the import/export commands and then looks a maximum of one line below it. It would be best to maintain at least one line between import/export commands and the code below it. Because the script is looking at one line below where it finds the command regardless of whether or not the next line is a new command. For example, This can be problematic if you save out your data and immediately put a print statement on the following line. The script will see the print line, identify the text in between the quotes and add it to the JSON object.
