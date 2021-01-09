library(tidyverse)

analytic = readRDS("./data/analytic.rds")
test = readRDS("./data/test.rds")

analytic %>% summarise_all(mean)
