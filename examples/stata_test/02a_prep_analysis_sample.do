global root "E:/program_evaluation"
include "$root/code/00_set_paths.do" // Places code from source file and places it in the body 
local name analysis_sample
local program wioa_adults 
log using "$code/`program'_`name'_log_file.smcl", replace // Log files 

foreach word in WIOAT1A WIOAT3 { 
    use "E:/Projects/CAAL-Skills/main_analysis/3_clean/2_WSB/2b_clean_`word'_part_analysis" if enter_quarter >= 29, clear 

    merge m:1 zip using "$temp/zip_county_crosswalk"
    save "$temp/`word'", replace 
}

append using "$temp/WIOAT1A"

save "$analysis/`program'_`name'", replace 
log close 

