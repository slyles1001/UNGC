require("RPostgreSQL")
library("RPostgreSQL")

# loads the PostgreSQL driver
drv <- dbDriver("PostgreSQL")
# creates a connection to the postgres database
# note that "con" will be used later in each connection to the database
"dbname='ungc_test' user='ducttapecreator' host='localhost' "
con <- dbConnect(drv, dbname = "ungc_test", host='localhost', user='ducttapecreator')

# check for the cartable
dbExistsTable(con, "ungc")
dbGetQuery(con, 'select distinct global_compact_status from ungc')

df_postgres <- dbGetQuery(con, "SELECT employees from UNGC 
                          where global_compact_status ='delisted'
                          limit 20;")

df_postgres

# Basic Graph of the Data
# require(ggplot2)
# ggplot(df_postgres, aes(x = as.factor(cyl), y = mpg, fill = as.factor(cyl))) + 
#  geom_boxplot() + theme_bw()



