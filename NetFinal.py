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
    x = {}
    with open(fname) as f:
        for line in f:
          s = line.split('\t')
          #print(s[3][:-1])
          # the \n char only counts as 1 letter, hence -1
          x[s[3]] = (s[1], s[2])
    f.closed
    return(x)

#st = "SELECT name, date from active where sector like 'Chem%' limit 20;"
    
def cleaned(country):
  '''takes a crappy padded string and returns the
  not padded version'''
  i = 0
  while country[i] + country[i+1] != '  ':
    i += 1
  return(country[:i]+'\n')

def writecountries():
  sel = "select distinct(country) from active"
  sel = ungc_db.query(sel)
  with open('newcountries.txt', 'w') as nc:
    for country in sel:
      c2 = cleaned(country[0])
      nc.write(c2)
    nc.closed
  
a = read_gps("./gps.txt")
with open('newcountries.txt') as nc:
  for line in nc:
    print(a[line])

#print(a[0])
