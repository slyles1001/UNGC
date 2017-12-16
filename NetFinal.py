# Seth Lyles
# NLT Final project
# 12.14.17

import numpy as np
from gurobipy import *
from graphs import *
import time

def get_dmat(fname = "dmat.txt"):
  x = []
  with open(fname) as f:
    for line in f:
      tmp = line[:-1].split(" ")
      x.append(list(map(int, tmp)))
  f.closed
  return(x)

def get_countries(fname = "newcountries.txt"):
  x = []
  with open(fname) as f:
    for line in f:
      x.append(line[:-1])
  f.closed
  return(x)

def get_emps(fname = "emp.txt"):
  d = {}
  with open(fname) as f:
    for line in f:
      
      x = line[:-1].split(",")
      # file reads in as:
      # country chemployees forestemploy  pharmploy
      # make dict with country as key, tuple of vals as val
      tmp = (x[1], x[2], x[3])
      d[x[0]] = list(map(int, tmp))
  f.closed
  return(d)

def split_sectors(emps = get_emps()):
  ''' Reads in file of # employes per country per sector, and returns
  array of 3 "weights" -- like [h_chem, h_forest, h_pharm] '''
  cl = sorted(emps.keys())
  bysec = []#np.array()
  for country in cl:
    bysec.append(list(emps[country]))
    
  return(np.transpose(bysec))  

def test_split():
  x = split_sectors()
  for i in x:
    print(i)

def ifelse(statement, t, f):
  '''ifelse like in R, which i like so here it is.'''
  if statement:
    return(t)
  else:
    return(f)

def p_median(var, d, h, p, countries):
    '''var = # nodes, d = graph matrix, 
        h = node weight vec, p = number of facilities
    '''
    m = Model()

    y = {}
    #W = m.addVar(lb = 0, name='W')
    x = m.addVars(range(var), name='Facility', vtype=GRB.BINARY)
    for i in range(var):
        for j in range(var):
            y[(i,j)] = m.addVar(name='y(%s,%s)'%(i,j), lb = 0)
            
    print(str(y[(0,1)]))
    m.update()
    m.modelSense=GRB.MINIMIZE
    m.setObjective(quicksum(quicksum(np.log(h[i] + 1)  * d[i][j] * y[(i, j)] for j in range(var)) for i in range(var)))
    m.update()

    m.addConstr(quicksum(x[j] for j in range(var)) == p)
    m.addConstrs(quicksum(y[(i,j)] for j in range(var)) == 1 for i in range(var))
    # it was picking 0s but i think it was because the above constraint was missing
    # m.addConstrs(x[j] <= bool(h[j]) for j in range(var))

    m.addConstrs(y[(i,j)] <= x[(j)] for j in range(var) for i in range(var))
  
    m.update()
    m.optimize()

    def printSolution(m, countries):
        obj = 0
        outs = []
        xvals = []
        if m.status == GRB.Status.OPTIMAL:
            print('Optimal objective value: %g' % m.ObjVal)
            obj = m.ObjVal
            for i, v in enumerate(m.getVars()):
                if v.VarName.split()[0][0] != 'y':
                    if v.x > 0.0001:
                        print('%s %d %g' % (countries[i], h[i], v.x))
                        outs.append(countries[i])
                        xvals.append(v.x)
            return [obj, outs, xvals]
        else:
            print('No solution')

    x = printSolution(m, countries)
    return(x)
  
def main():
  #l = list([(1, 2), (1, 3), (2, 3), (2, 4)])
  #d = model.addVars(l, name="d")
  sectors = ("Chemicals","Forestry & Paper","Pharmacy & Biotechnology")
  dmat = get_dmat()
  countries = get_countries()
  emps = get_emps()
  var = len(countries)
  W = split_sectors()
  with open('output.txt', 'w') as outfile:
    for i in range(3):
      p = i+1
      for i, weight in enumerate(W):
        t1 = time.clock()
        outputs = p_median(var, dmat, weight, p, countries)
        t2 = time.clock()
        #outfile.write("obj = %g, " % outputs[0])
        #outfile.write(" %s," % len(outputs[1]))
        outfile.write("Objective: %(g)s\n p: %(p)s\n Sector: %(s)s\n Runtime: %(r)f\n" % \
            {'g':outputs[0], 'p': p, 's': sectors[i], 'r':(t2 - t1)})
        #outfile.write("%g, " % outputs[0])
        outfile.write("Activated nodes:\n")
        # # writes the indices of facility sites
        for node in outputs[1]:
            outfile.write("%s " % node)
        outfile.write('\n\n')

  return(0)
  
#main()
  
def make_layout(p):
  layout = dict(
        title = 'Central meeting location<br>p = %d' % (p + 1),
        #showlegend = False,
        geo = dict(
            resolution = 150,
            showland = True,
            showlakes = True,
            showcountries = True,
            showocean = True,
            countrywidth = 0.5,
            #countrycolor = 'rgb(255, 255, 255)',
            landcolor = 'rgb(230, 145, 56)',
            lakecolor = 'rgb(0, 255, 255)',
            oceancolor = 'rgb(0, 255, 255)',
            projection = dict( type="Natural Earth" ),
            coastlinewidth = 1,
            lataxis = dict(
                range = [ -80, 80 ],
                showgrid = False

            ),
            lonaxis = dict(
                range = [-160, 160],
                showgrid = False
            ),
        )
    )
  return(layout)

def sphere_layout(p):
  layout = dict(
      title = 'Flight Routes for p = %d<br>(Click and drag to rotate)' % (p+1),
     # showlegend = False,
      geo = dict(
          showland = True,
          showlakes = True,
          showcountries = True,
          showocean = True,
          countrywidth = 0.5,
          landcolor = 'rgb(230, 145, 56)',
          lakecolor = 'rgb(0, 255, 255)',
          oceancolor = 'rgb(0, 255, 255)',
          projection = dict(
              type = 'orthographic',
              rotation = dict(
                  lon = -100,
                  lat = 40,
                  roll = 0
              )
          ),
          lonaxis = dict(
              showgrid = True,
              gridcolor = 'rgb(102, 102, 102)',
              gridwidth = 0.5
          ),
          lataxis = dict(
              showgrid = True,
              gridcolor = 'rgb(102, 102, 102)',
              gridwidth = 0.5
          )
      )
  )
  return(layout)
  
def plotit():
  p1 = [['austria'], ['austria'],['austria']]
  p2 = [['myanmar','switzerland'], ['paraguay', 'poland'], ['czechia', 'peru']]
  p3 = [['austria', 'ecuador', 'myanmar'], ['germany', 'paraguay', 'thailand'],\
        ['austria', 'bangladesh', 'peru']]
  x = [p1,p2,p3]
  for i in range(3):
    layout = make_layout(i)
    sp_layout = sphere_layout(i)
    print(len(x[i][0]))
    data = add_routes(c_facils = x[i],  \
          dmat = get_dmat(), emps = get_emps())
    url = plots(data, layout, i)
    url2 = plots(data, sp_layout, i+3)
  
plotit()  
  
  
  
  
  
  
