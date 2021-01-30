library(tidyverse)

dt <- tibble(
    "A" = c(rep(0, 1000)),
    "B" = c(rep(1, 1000))
)

sqlCall <- "SELECT * FROM db.dba.hello FROM something.dba.hi"
saveRDS(
    dt,
    "./data/analytic.rds"
)
saveRDS(dt, "./data/test.rds")
saveRDS(dt, "./data/notUsedData.rds")