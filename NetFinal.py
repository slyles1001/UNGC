#import matplotlib.pyplot as plt
import dbase as db
#import pandas as pd
import numpy as np

def test_connection():
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
  
def test_gps_countries():
  a = read_gps("./gps.txt")
  with open('newcountries.txt') as nc:
    for line in nc:
      print(a[line])

def haversine(a, b):
  x = [float(a[0]), float([a[1]])
  y = [float(b[0]), float([b[1]])
  R = 6371 # km
  x = np.radians(x);
  y = np.radians(y);
  # shouldn't want both of these, right?
  dlat = np.radians(y[0] - x[0]);
  dlon = np.radians(y[1] - y[2]);

  var a = Math.sin(Δφ/2) * Math.sin(Δφ/2) +
          Math.cos(φ1) * Math.cos(φ2) *
          Math.sin(Δλ/2) * Math.sin(Δλ/2);
  var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  
  var d = R * c;
