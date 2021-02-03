global root "E:/program_evaluation"
include "$root/code/00_set_paths.do" // Places code from source file and places it in the body 
local name entropy_balancing
local program wioa_adults 

log using "$code/`program'_`name'_log_file.smcl", replace // Log files 

save "$temp/`program'_`name'_entropy_weights", emptyok replace 
save "$temp/`program'_`name'_balance_check", emptyok replace 

* Check for ebalance package on the system 
capture which ebalance 
if _rc { 
    display as error "Please install the ebalance package"
}

use "$analysis/analysis_sample", clear 
levelsof quarter_zip, local(qzip)

foreach q of local qzip { 
    use $analysis/analysis_sample if quarter_zip == "`q'", clear 

    if r(N) == `condition' { 
        keep puid quarter_zip weight_entropy 
        append using "$temp/`name'_entropy_weights"
        save "$temp/`program'_`name'_entropy_weights", replace 
    }

    else { 
        keep quarter_zip 
        append using "$temp/`program'_`name'_balance_check"
        save "$temp/`program'_`name'_balance_check", replace 
    }
}

use "$temp/`program'_`name'_entropy_weights", clear 
merge 1:1 puid using "$analysis/`program'_analysis_sample"

* Output table 1 to Stata matrix 
putexcel set "tables/`name'_balance_table", replace // output matrix to Excel 
putexcel A1 = matrix(balance_table)

log close 