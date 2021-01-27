library(tidyverse)

analytic = readRDS("./data/analytic.rds")

analytic %>% summarise_all(mean)
