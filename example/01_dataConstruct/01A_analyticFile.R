library(tidyverse)

dt = tibble(
    "A" = c(rep(0, 1000)),
    "B" = c(rep(1, 1000))
    )

saveRDS(dt,
    "./data/analytic.rds")
saveRDS(dt, "./data/test.rds")
