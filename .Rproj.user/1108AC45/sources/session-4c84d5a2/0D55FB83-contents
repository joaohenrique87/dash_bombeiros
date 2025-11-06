library(tidyverse)
library(openxlsx)
library(ggplot2)
library(tidyr)
library(scales)
library(here)
library(lubridate)
install.packages("RSQLite")
library(RSQLite)

dados <- "dados"

if (!dir.exists(dados)) {
  dir.create(dados)
}

ds <- "fema/firefighter-fatalities"
download_bd <- sprintf("kaggle datasets download -d %s -p %s --unzip", ds, dados)
system(download_bd)

setwd(here(dados))

a <- read_csv("database.csv")

str(a)

a <- a %>% select(-14) %>% rename(
  nome = "First Name",
  sobrenome = "Last Name",
  idade = "Age",
  patente = "Rank",
  classificacao = "Classification",
  data_inc = "Date of Incident",
  data_mor = "Date of Death",
  causa = "Cause Of Death",
  natu = "Nature Of Death",
  servico = "Duty",
  atividade = "Activity",
  sos = "Emergency",
  tipo_local = "Property Type"
) %>% drop_na()

a <- a %>% mutate(data_inc = mdy(data_inc),
                  data_mor = mdy(data_mor))

a <- a %>% mutate(ano_inc = year(data_inc),
                  ano_mor = year(data_mor),
                  diferenca = as.numeric(abs(data_inc - data_mor)))

write_csv(a, "database.csv")

db <- "bombeiros.db"
con <- dbConnect(SQLite(), db)

dbWriteTable(con, "mortes", a, overwrite = TRUE)

dbDisconnect(con)

