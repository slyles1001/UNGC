#import matplotlib.pyplot as plt
import dbase as db
#import pandas as pd
import numpy as np
import string

def fix(stri, fu = 0):
	'''stri to clean for db entry
		db not so good with apostrophes
		get rid of spaces and ., other punctuation too, preventatively
		may cause complications for country ID but postgres doesn't case sensitive'''
	# Python interprets 'None' as None for some reason;
	# 'None' was listed as reason for delisting so script errored out.
	def fux(st):
		return st.replace(" ", "_")
		
	if stri is not None:
		stri = stri.lower()
		stri = "".join(l for l in stri if l not in string.punctuation)
		if(fu):
			stri = fux(stri)
		if(stri[-1] == '\n'):
		  stri = stri[:-1]
		return(stri)
	else:
		return("none")
		
def connect():
  connect_str = "dbname='NetFinal' user='ducttapecreator' host='localhost' " #+ \
  			 # "password='OLIVIA'"
  
  #other = "SELECT count(name) from UNGC where country~*'united states' and date_due>='%s' and date_due<'%s';" % (yr, yr+10000)
  
  ungc_db = db.db(connect_str)
  def test_connection():
    st = "SELECT count(name) from ungc where sector like 'Pharma%';"
    v = ungc_db.query(st)
    print(v)
    st = "SELECT count(name) from ungc where sector like 'Fore%';"
    w = ungc_db.query(st)
    print(w)
    st = "SELECT count(name) from ungc where sector like 'Chem%';"
    x = ungc_db.query(st)
  
  return(ungc_db)

def read_gps(fname="./gps.txt"):
    x = {}
    with open(fname) as f:
        for line in f:
          s = line.split('\t')
          x[fix(s[3])] = (float(s[1]), float(s[2]))
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
    # only care about the countries that are active in that industry
    # cuts the list down from 154 to 63
    sel = """select distinct(country) from UNGC 
              where global_compact_status = 'active'
              and (sector ~* 'pharm' or sector ~* 'forest'
              or sector ~* 'chem') """
    ungc_db = connect()
    sel = ungc_db.query(sel)
    with open('newcountries.txt', 'w') as nc:
      for country in sorted(sel):
        c2 = country[0] + "\n" # cleaned(country[0])
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
    
  def get_emp_count(country, sector):
    ''' input a country and a sector, returns the number of employees that sector has in that country
    '''
    ungc_db = connect()
    q = """select sum(employees) from UNGC 
              where global_compact_status='active' and 
              country ~* '%s' and
              sector ~* '%s'
      """ % (country, sector)
    sel = ungc_db.query(q)[0][0]
    if sel != None:
      return(sel)
    else:
      return("NA")
  
  def test_emp_count():
    sector = ("chem", "forestry", "pharma")
    for s in sector:
      x = (get_emp_count('france', s),)
    print(x)
  #test_emp_count()
  
  def string_print(l):
    ''' takes a list of not strings and returns a list of strings'''
    x = []
    for i in l:
      x.append(str(i))
    return(x)
  
  def write_emp_count(emp_tally):
    sector = ("chem", "forestry", "pharma")
    b = read_countries()
    d = {}
    
    for country in b:
      emp_count = ()
      for sec in sector:
        emp_count += (get_emp_count(country, sec), )
      if emp_count != ('NA','NA','NA'):
        d[country] = emp_count
    if emp_tally:
      with open("emp.txt", "w") as e:
        for country in sorted(d.keys()):
          e.write(country + "  " +
          "  ".join(string_print(d[country])) + "\n")
      e.closed
    return(d)
  
  #write_emp_count(emp_tally)
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
      try:
        row.append(haversine(a[country], a[b[i]]))
      except KeyError:
        print(country, b[i])
    dx.append(row)
  return(dx)

def read_countries(fname = 'newcountries.txt'):
  ''' reads country list from file (from db)
  returns list containing countries '''
  x = []
  with open(fname) as nc:
      for line in nc:
        x.append(line[:-1])
  nc.closed
  return(x)
#import gurobipy as gb

#file_creation(0,1, 0)  

