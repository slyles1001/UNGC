#import matplotlib.pyplot as plt
#import scraping_dict as sd
#import pandas as pd
#import numpy as np


#connect_str = "dbname='testpython' user='ducttapecreator' host='localhost' " #+ \
#			  "password='OLIVIA'"

# use our connection values to establish a connection
#conn = psycopg2.connect(connect_str)
# create a psycopg2 cursor that can execute queries
#cursor = conn.cursor()

#other = "SELECT count(name) from UNGC where country~*'united states' and date_due>='%s' and date_due<'%s';" % (yr, yr+10000)

def read_gps(fname):
    x = []
    with open(fname) as f:
        s = f.readline().split('\t')
        x.append(s[1:])
    f.closed
    return(x)

a = read_gps("./gps.txt")
print(a[0])