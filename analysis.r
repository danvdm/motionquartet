rm(list = ls())
library(tidyverse)

df <- data.frame(t(read.csv("/Users/daniel/Documents/Arbeit/PHD/Experiment/test.csv")[2:9]))
df

df <- df %>% mutate(switch = X2*rep(c(1, -1), 4))

plot(df[,1], df[,3]/df[,2], type = "l", ylim = c(0, 2))
abline(h = 1)

