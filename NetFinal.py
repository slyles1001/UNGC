#import matplotlib.pyplot as plt
import dbase as db
#import pandas as pd
#import numpy as np


connect_str = "dbname='testpython' user='ducttapecreator' host='localhost' " #+ \
			 # "password='OLIVIA'"

#other = "SELECT count(name) from UNGC where country~*'united states' and date_due>='%s' and date_due<'%s';" % (yr, yr+10000)

ungc_db = db.db(connect_str)
st = "SELECT count(name) from active where sector like 'Pharma%';"
v = ungc_db.query(st)
print(v)
st = "SELECT count(name) from active where sector like 'Fore%';"
w = ungc_db.query(st)
print(w)
st = "SELECT count(name) from active where sector like 'Chem%';"
x = ungc_db.query(st)

def read_gps(fname):
    x = []
    with open(fname) as f:
        s = f.readline().split('\t')
        x.append(s[1:])
    f.closed
    return(x)
    
st = "SELECT name, date from active where sector like 'Chem%' limit 20;"
#ungc_db.query(st)
#print(ungc_db)


#a = read_gps("./gps.txt")
#print(a[0])
