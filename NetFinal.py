# Seth Lyles
# NLT Final project
# 12.14.17

import numpy as np
from gurobipy import *


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

def guropt(var, d, h, k, countries):
    '''var = # nodes, d = graph matrix, 
        h = node weight vec, k = number of facilities
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

    m.addConstr(quicksum(x[j] for j in range(var)) == k)
    m.addConstrs(quicksum(y[(i,j)] for j in range(var)) == 1 for i in range(var))
    m.addConstrs(x[j] <= bool(h[j]) for j in range(var))

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
                        outs.append(v.VarName)
                        xvals.append(v.x)
            return [obj, outs, xvals]
        else:
            print('No solution')

    x = printSolution(m, countries)
    return(x)
  
def main():
  #l = list([(1, 2), (1, 3), (2, 3), (2, 4)])
  #d = model.addVars(l, name="d")
  dmat = get_dmat()
  countries = get_countries()
  emps = get_emps()
  var = len(countries)
  W = split_sectors()
  with open('output.txt', 'w') as outfile:
    for i in range(3):
      k = i+1
      for weight in W:
        outputs = guropt(var, dmat, weight, k, countries)
        outfile.write("%g, " % outputs[0])
  return(0)
  
main()
  
  
  
