global root "E:/program_evaluation"
include "$root/code/00_set_paths.do" // Places code from source file and places it in the body 
local name regressions 
local program wioa_adults 

log using "$code/`program'_`name'_log_file.smcl", replace // Log files 

use "$temp/`program'_entropy_weights", clear 
merge 1:1 puid using "$analysis/`program'_analysis_sample"

* Do regression goodness 
putexcel set "$tables/`program'_regression", replace 
putexcel A1 = matrix(regression)