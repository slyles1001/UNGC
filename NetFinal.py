# Seth Lyles
# NLT Final project
# 12.14.17

import numpy as np
from gurobipy import *


def get_dmat(fname = "dmat.txt"):
  x = []
  with open(fname) as f:
    for line in f:
      x.append(list(map(int, line)))
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
      d[x[0]] = (x[1], x[2], x[3])
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

def guropt(var, l, h, k):
    '''var = # nodes, l = graph matrix, 
        h = node weight vec, k = number of facilities
    '''
    m = Model()

    y = {}
    W = m.addVar(lb = 0, name='W')
    x = m.addVars(range(var), name='Facility', vtype=GRB.BINARY)
    for i in range(var):
        for j in range(var):
            y[(i,j)] = m.addVar(name='y(%s,%s)'%(i,j), lb = 0)

    m.update()
    m.modelSense=GRB.MINIMIZE
    m.setObjective(quicksum(quicksum(quicksum(h[i]*l[i][j]*y[(i,j)] for j in range(var)) for i in range(var)))
    m.update()

    for i in range(var):
        m.addConstr(quicksum(y[(i,j)] for j in range(var)) == 1)

    for i in range(var):
        for j in range(var):
            m.addConstr(y[(i,j)] <= x[(j)])

    m.update()
    m.optimize()

    def printSolution(m):
        obj = 0
        outs = []
        xvals = []
        if m.status == GRB.Status.OPTIMAL:
            print('Optimal objective value: %g' % m.ObjVal)
            obj = m.ObjVal
            for i, v in enumerate(m.getVars()):
                if v.VarName.split()[0][0] != 'y':
                    if v.x > 0.0001:
                        print('%s %g' % (v.VarName, v.x))
                        outs.append(v.VarName)
                        xvals.append(v.x)
            return [obj, outs, xvals]
        else:
            print('No solution')

    x = printSolution(m)
    return(x)
  
def main():
  #l = list([(1, 2), (1, 3), (2, 3), (2, 4)])
  #d = model.addVars(l, name="d")
  dmat = get_dmat()
  countries = get_countries()
  emps = get_emps()
  var = len(countries)
  W = split_sectors()
  for weight in W:
    guropt(var, dmat, )
  
  
  
  
  
  
