# About 

The following is a list of most commonly used commands for data management in Stata. The syntax patterns are taken directly from the [Stata manual](https://www.stata.com/manuals/r.pdf). I recommend googling "stata command manual" for the relevant PDF chapter.

The most general syntax pattern is: command filename [, options]. In Stata manuals, words in parentheses are optional arguments. The "varlist" option lets users specify as many variables available in the current dataset. Included below are examples where commands include mandatory modifiers that either change action or are part of the original program design.

# Local and global variables

Locals are typically used in script-specific contexts and globals across the project. Locals are deleted after script execution and globals can hang around if not explicitly deleted. 

## Global 

`global root "E:/program_evaluation"` 
	
## Local 

`local program wioa_adults` 

save "$root/`name'_analysis_file" 

# Load datasets

## Load Stata-format dataset

`use filename [, clear nolabel]`

## Load subset of Stata-format dataset

`use [varlist] [if] [in] using filename [, clear nolabel]`

# Import non-Stata data

## Excel

### Load an Excel file

`import excel [using] filename [, import_excel_options]`

## Load subset of variables from an Excel file

`import excel extvarlist using filename [, import_excel_options]`

# Save datasets 

## Save Stata-format dataset

`save filename [, replace]`

## Save subset of Stata-format dataset

`save [varlist] [if] [in] using filename [, replace]`

# Export non-Stata data

## Excel

### Save data in memory to an Excel file

`export excel [using] filename [if] [in] [, export_excel_options]`

### Save subset of variables in memory to an Excel file

`export excel [varlist] using filename [if] [in] [, export_excel_options]`

## Delimited

### Load a delimited text file

`import delimited [using] filename [, import_delimited_options]`

### Rename specified variables from a delimited text file

`import delimited extvarlist using filename [, import_delimited_options]`

### Save data in memory to a delimited text file

`export delimited [using] filename [if] [in] [, export_delimited_options]`

### Save subset of variables in memory to a delimited text file

`export delimited [varlist] using filename [if] [in] [, export_delimited_options]`

## Others

There are other data-format-specific options available for a look [here](https://www.stata.com/manuals/dimport.pdf#dimport). 

# Merge on variables (joins in dplyr)

## One-to-one merge on specified key variables

`merge 1:1 varlist using filename [, options]`

## Many-to-one merge on specified key variables

`merge m:1 varlist using filename [, options]`

## One-to-many merge on specified key variables

`merge 1:m varlist using filename [, options]`

## Many-to-many merge on specified key variables (not generally recommended!)

`merge m:m varlist using filename [, options]`

## One-to-one merge by observation

`merge 1:1 _n using filename [, options]`

# Append (row_bind in dplyr)

`append using filename [filename ...] [, options]`

# Write results to Excel spreadsheet 

`putexcel set filename [, set_options]`

# Graphs (honestly, a dumpster fire in Stata)

`graph export newfilename.suffix [, options]`