global root "E:/program_evaluation"
include "$root/code/00_set_paths.do" // Places code from source file and places it in the body 
local name zip_county_crosswalk

log using "$code/`name'_log_file.smcl", replace // Log files 

import delimited "$source/us_cities_counties.csv", clear 
save "$temp/city_county_crosswalk", replace 

use "$source/ca_zip_to_county_2016", clear 
tempfile mdrc 
save `mdrc'

import excel "$source/ZIP_COUNTY_122020", sheet("ZIP_COUNTY_122020") cellrange(A1:B54195) clear 

merge 1:1 zip fips county using `mdrc'
keep if _merge == 3 

save "$temp/`name''", replace 
log close 

