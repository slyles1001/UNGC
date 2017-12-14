#import matplotlib.pyplot as plt
import dbase as db
#import pandas as pd
import numpy as np

def connect():
  connect_str = "dbname='NetFinal' user='ducttapecreator' host='localhost' " #+ \
  			 # "password='OLIVIA'"
  
  #other = "SELECT count(name) from UNGC where country~*'united states' and date_due>='%s' and date_due<'%s';" % (yr, yr+10000)
  
  ungc_db = db.db(connect_str)
  def test_connection():
    st = "SELECT count(name) from active where sector like 'Pharma%';"
    v = ungc_db.query(st)
    print(v)
    st = "SELECT count(name) from active where sector like 'Fore%';"
    w = ungc_db.query(st)
    print(w)
    st = "SELECT count(name) from active where sector like 'Chem%';"
    x = ungc_db.query(st)
  
  return(ungc_db)

def read_gps(fname="./gps.txt"):
    x = {}
    with open(fname) as f:
        for line in f:
          s = line.split('\t')
          #print(s[3][:-1])
          x[s[3]] = (float(s[1]), float(s[2]))
    f.closed
    return(x)

def cleaned(country):
  '''takes a crappy padded string and returns the
  not padded version'''
  i = 0
  while country[i] + country[i+1] != '  ':
    i += 1
  return(country[:i]+'\n')
  
def file_creation(country_list, distance, emp_tally):
  ''' function to hide all the testing and file creating functions 
      params are booleans to create the file or not
  '''
  def writecountries():
    ''' Writes a list of countries to file. Based on UNGC data, not gps.
    '''
    sel = "select distinct(country) from active"
    ungc_db = connect()
    sel = ungc_db.query(sel)
    with open('newcountries.txt', 'w') as nc:
      for country in sel:
        c2 = cleaned(country[0])
        nc.write(c2)
      nc.closed
      
  if country_list: # 
    writecountries()  
    
  def test_gps_countries():
    ''' testing the countries to see if the names match in DB and GPS '''
    a = read_gps()
    with open('newcountries.txt') as nc:
      for line in nc:
        print(a[line])
  #test_gps_countries()
  
  def test_hav():
    ''' Make sure the haversine function works, or well enough '''
    a = read_gps()
    b = sorted(a.keys())
    x = b[0]
    y = b[1]
    print(x,y)
    d = haversine(a[x], a[y])
    print(d)
    x = b[3]
    y = b[7]
    d = haversine(a[x], a[y])
    print(x,y)
    print(d)
  #test_hav()
  
  def write_dist(file):
    dx = fill_dist()
    with open(file, 'w') as f:
      for line in dx:
        s = ' '.join(line)
        f.write(s + '\n')
    f.closed
  
  if distance:
    write_dist('dmat.txt')
    
  def get_info(country, sector):
    ''' input a country and a sector, returns the number of employees that sector has in that country
    '''
    ungc_db = connect()
    sel = "select sum(country) from active"
    sel = ungc_db.query(sel)
    
  return(0)
  
def haversine(a, b):
  '''a and b are coordinate tuples 
  returns the great circle distance
  '''
  R = 6371 # km
  x = np.radians(a)
  y = np.radians(b)

  dlat = y[0] - x[0]
  dlon = y[1] - x[1]
  dsig = 2*np.arcsin(
          np.sqrt(
            np.sin(dlat/2)**2 +
            np.cos(x[0]) * np.cos(y[0]) * np.sin(dlon/2)**2
          )
        )
  d = R * dsig
  # to print arrays we must convert to string...
  return(str(int(d)))

def fill_dist(): 
  ''' returns an adjacency matrix using great distance calc.
  from gps coordinates '''
  a = read_gps()
  b = read_countries()
  dx = []
  for country in b:
    row = []
    for i in range(len(b)):
      row.append(haversine(a[country], a[b[i]]))
    dx.append(row)
  return(dx)

def read_countries(fname = 'newcountries.txt'):
  ''' reads country list from file (from db)
  returns list containing countries '''
  x = []
  with open(fname) as nc:
      for line in nc:
        x.append(line)
  nc.closed
  return(x)
#import gurobipy as gb

#file_creation(False, False, True)  

