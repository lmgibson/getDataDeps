assert "$root" != "" 

global code "$root/code"
global graphs "$root/output/graphs"
global tables "$root/output/tables"
global analysis "$root/data/analysis" // Finalized analysis files go here 
global source "$root/data/source" // Non-confidential, shareable primary data files 
global temp "$root/data/temp" // Temporary storage for files 

cd $root
display "$root"