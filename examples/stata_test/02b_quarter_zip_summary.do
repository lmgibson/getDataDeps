global root "E:/program_evaluation"
include "$root/code/00_set_paths.do" // Places code from source file and places it in the body 
local name quarter_zip_summary  
local program wioa_adults 

log using "$code/`program'_`name'_log_file.smcl", replace // Log files 

use "$analysis/`program'_analysis_sample", clear 

*Histogram data prep 
graph export "$graphs/`program'_`name'", as(png) replace 

