





import matplotlib.pyplot as plt
import scraping_dict as sd
import pandas as pd
import numpy as np

ungc_db = sd.db()

#st = "SELECT count(name), count(distinct sector), count(distinct org_type) from UNGC where date_joined < '%s' and date_due >= '%s' and country='%s' limit 20;" % (20100101, 20110101, 'brazil')
yr = 20000101
joins = []
leaves = []
total = []
yrs = []
for i in range(16):
    active = "SELECT count(name) from UNGC where date_joined>='%s' and date_joined<'%s' and country~*'united states';" % (yr, yr+10000)
    #print(yr, yr + 10000)
    ungc_db.query(active)
    joins.append(ungc_db.query_results[0][0])
    other = "SELECT count(name) from UNGC where country~*'united states' and date_due>='%s' and date_due<'%s';" % (yr, yr+10000)
    ungc_db.query(other)
    leaves.append(ungc_db.query_results[0][0])
    exist = "SELECT count(name) from UNGC where date_joined<'%s' and country~*'united states'and date_due > '%s';" % (yr+10000,yr+10000)
    ungc_db.query(exist)
    total.append(ungc_db.query_results[0][0])
    yrs.append(yr)
    yr = yr + 10000
    

y = pd.Series(yrs)


d = {'Joined' : pd.Series(joins, index=y), 'Left' : pd.Series(leaves, index=y), 'Exist' : pd.Series(total, index=y)}
pl = pd.DataFrame(d)
pl = pl.cumsum()
pl.plot.bar()
plt.show()