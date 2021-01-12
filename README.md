getDataDeps-R is a command line tool that maps data dependencies across R files in your project.
The tool is currently a work in progress but when it is complete it can be ran from the root project folder
and will return a json object consisting of filenames and the data that each file outputs or reads in.

If the code is in the root of your project, it can be run by:
`python getDataDeps.py`

Which will iterate through your entire project folder, extract files that end in ".R", and then collect information
on data imports and data exports.
