#GLOBAL PARTNERSHIPS

library(igraph)
library(stringr)
setwd("~/UNGC")

#### Data initialization ####
UNGC <- read.delim("~/UNGC/UNGC.txt", header=FALSE, comment.char="#")
#View(UNGC)

# isolate Name of unit, type of unit, sector of unit, country of origin 
name = UNGC[,1]
type = UNGC[,2]
sector = UNGC[,3]
country = UNGC[,4]
year = UNGC[,5]

# number of active entries in UNGC as of 26/04/2016
entry_count <- length(name)

# Compact country list to show no repeats
country_list <- levels(sort(country))
country_count <- length(country_list)
#country_list

# Compact type list
type_list <- levels(sort(type))
type_count <- length(type_list)
#type_list

# Compact sector list
sector_list <- levels(sort(sector))
sector_count <- length(sector_list)
#sector_list

# might as well init all graphs at once
all_names <- all_countries <- all_types <- all_sectors <- make_empty_graph()

# fill graph object with disconnected node foreach entity
for (i in 1:entry_count){
  all_names = add_vertices(all_names, 1, name=as.character(name[i]))
}

# make sure all our nodes were added ok
summary(all_names)
stopifnot(vcount(all_names) == entry_count)

# fill graph object with disconnected node foreach country
for (i in 1:country_count){
  all_countries <- add_vertices(all_countries, 1, name=as.character(country_list[i]))
}

# make sure all our nodes were added ok
stopifnot(vcount(all_countries) == country_count)
summary(all_countries)

# fill graph object with disconnected node foreach type
for (i in 1:type_count){
  all_types <- add_vertices(all_types, 1, name=as.character(type_list[i]))
}

# make sure all our nodes were added ok
stopifnot(vcount(all_types) == type_count)
summary(all_types)

for (i in 1:sector_count){
  all_sectors <- add_vertices(all_sectors, 1, name=as.character(sector_list[i]))
}

# make sure all our nodes were added ok
stopifnot(vcount(all_sectors) == sector_count)
summary(all_sectors)

#### Adding Edges ####

country_to_sector <- make_empty_graph()

for(i in 1:entry_count){
  
  
  
}



