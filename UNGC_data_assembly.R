#GLOBAL PARTNERSHIPS

library(igraph)
library(stringr)
setwd("~/UNGC/R scripts/UNGC")

UNGC <- read.delim("~UNGC/R scripts/data.txt", header=FALSE, comment.char="#")
View(UNGC)
# Create Type/Country/Year/Sector/Area
type = UNGC[,2]
country = UNGC[,4]
year = UNGC[,5]
sector = UNGC[,3]
name = UNGC[,1]

# Number of types overall
sum(str_count(type, "Academic"))
sum(str_count(type, "Business Association Global"))
sum(str_count(type, "Business Association Local"))
sum(str_count(type, "City"))
sum(str_count(type, "Company"))
sum(str_count(type, "Foundation"))
sum(str_count(type, "Micro Enterprise"))
sum(str_count(type, "NGO Global"))
sum(str_count(type, "NGO Local"))
sum(str_count(type, "Public Sector Organization"))
sum(str_count(type, "Small or Medium-sized Enterprise"))

# Country (149) and type (12) levels
alphab_country <- sort(country, decreasing = FALSE)
country_level <- levels(alphab_country)
country_level

alphab_type <- sort(type, decreasing = FALSE)
type_level <- levels(alphab_type)
type_level

all_data = make_empty_graph()


for (i in 1:9005){
  all_data = add_vertices(all_data, 1, name=as.character(name[i]))#, country=as.character(country[i]), year=as.character(year[i]), type=as.character(type[i]))
  
}
V(all_data)$name