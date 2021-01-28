library(tidyverse)

analytic <- readRDS("./data/analytic.rds")

analytic %>% summarise_all(mean)

write_csv(analytic, "./data/modeling.csv")