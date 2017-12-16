import plotly.plotly as py
import plotly.graph_objs as go
from NLT_preproc import *
import numpy as np
#from plotly.graph_objs import *
#from mpl_toolkits.basemap import Basemap

def add_routes(c_facils, dmat, emps):
  ''' c_facils is list of cities selected
      sector is one of 3 sectors
      dmat is distance adj matrix
      emps is dict with keys as countries and (chem, forest, pharma) weights
  '''
  x = []
  d = read_gps()
  sec_col = ['blue','green','red']
  secs = ['Chemicals', 'Forestry', 'Pharmaceuticals']
  cl = sorted(emps.keys())
  
  for sector in range(3):
    most = max(c[sector] for c in emps)
    for i, c in enumerate(cl):
      if emps[c][sector] > 0:
        msf = 1000000
        place = c_facils[0]
        for country in c_facils[sector]:
          current = cl.index(country)
          if dmat[current][i] < msf:
            msf = dmat[current][i]
            place = country
        x.append(go.Scattergeo(
          lat = [d[place][0], d[c][0]],
          lon = [d[place][1], d[c][1]],
          mode = 'lines',
          legendgroup = secs[sector],
          showlegend=False,
          line = dict(
            width = .5,#len(str(emps[c][sector]))/2,
            color = sec_col[sector],
          ),
        ))  
    x.append(go.Scattergeo(
          lat = [d[place][0], d[c][0]],
          lon = [d[place][1], d[c][1]],
          mode = 'lines',
          legendgroup = secs[sector],
          name = secs[sector],
          line = dict(
            width = .5,#len(str(emps[c][sector]))/2,
            color = sec_col[sector],
          ),
        ))  
  return(x)        
      
 
def plots(data, layout, p):
  # Get list of of coastline and country lon/lat traces
  #traces_cc = get_coastline_traces()+get_country_traces()
  #Data(traces_cc + data)
  fig = dict( data=data, layout=layout )
  url = py.plot( fig, filename='d3-great-circle-%d' % p )
  return(url)
 
def blah():  
  # # Make shortcut to Basemap object, 
  # # not specifying projection type for this example
  # #m = Basemap() 
  # 
  # # Make trace-generating function (return a Scatter object)
  # #def make_scatter(x,y):
  #     return Scatter(
  #         x=x,
  #         y=y,
  #         mode='lines',
  #         line=Line(color="black"),
  #         #width=.1,
  #         name=' '  # no name on hover
  #     )
  # 
  # # Functions converting coastline/country polygons to lon/lat traces
  # #def polygons_to_traces(poly_paths, N_poly):
  #     ''' 
  #     pos arg 1. (poly_paths): paths to polygons
  #     pos arg 2. (N_poly): number of polygon to convert
  #     '''
  #     traces = []  # init. plotting list 
  # 
  #     for i_poly in range(N_poly):
  #         poly_path = poly_paths[i_poly]
  #         
  #         # get the Basemap coordinates of each segment
  #         coords_cc = np.array(
  #             [(vertex[0],vertex[1]) 
  #              for (vertex,code) in poly_path.iter_segments(simplify=False)]
  #         )
  #         
  #         # convert coordinates to lon/lat by 'inverting' the Basemap projection
  #         lon_cc, lat_cc = m(coords_cc[:,0],coords_cc[:,1], inverse=True)
  #         
  #         # add plot.ly plotting options
  #         traces.append(make_scatter(lon_cc,lat_cc))
  #      
  #     return traces
  # 
  # # Function generating coastline lon/lat traces
  # #def get_coastline_traces():
  #     poly_paths = m.drawcoastlines().get_paths() # coastline polygon paths
  #     N_poly = 91  # use only the 91st biggest coastlines (i.e. no rivers)
  #     return polygons_to_traces(poly_paths, N_poly)
  # 
  # # Function generating country lon/lat traces
  # #def get_country_traces():
  #     poly_paths = m.drawcountries().get_paths() # country polygon paths
  #     N_poly = len(poly_paths)  # use all countries
  #     return polygons_to_traces(poly_paths, N_poly)
  
  
  #fs = ['myanmar','switzerland']
  #first = add_routes()
  pass
