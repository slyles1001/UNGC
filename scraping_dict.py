#Seth Lyles
#2016 June 22

from bs4 import BeautifulSoup
import urllib3, certifi, psycopg2, string
from dateutil.parser import parse
from timeit import default_timer as timer
import dbase as db


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
		return(stri)
	else:
		return("none")
# comment comment	
def data_getter(url):
	''' Returns the page data from URL '''
	ld = http.request("GET", url)
	sp = BeautifulSoup(ld.data, "lxml")
	return(sp)

def scrape_data(url):
	''' Finds the date that the entity became delisted at URL '''
	sp = data_getter(url)
	# Find all the relevant locations in web page source
	#name, date joined, and date due/delisted are in different locations
	nm = sp.find("header", {"class":"main-content-header"})
	start = sp.find("div", {"class":"company-information-since"})
	ldtext = sp.find("div",  {"class":"company-information-cop-due"})
	othertext = sp.find("div", {"class":"company-information-overview"})
	# all other data is together, so we make list of key and value
	keys = othertext.findAll("dt")
	vals = othertext.findAll("dd")
	
	# clean dates so they are accepted by db
	dd = parse(ldtext.time.string).strftime("%Y/%m/%d")
	dj = parse(start.time.string).strftime("%Y/%m/%d")
	
	# build dict so we can return only one thing
	#d = {'name': fix(nm.h1.string), 'date_due':dd, 'date_joined':dj}
	d = {"name": fix(nm.h1.string), "date_due":dd, "date_joined":dj}
	
	# add rest of data to dict
	for i in range(len(keys)):
		#d[fix(keys[i].string)] = fix(vals[i].string)
		d[fix(keys[i].string, 1)] = fix(vals[i].string)
		
	# return dictionary of keys (name, country, sector, etc.) with assoc. values ("tims_auto", "spain", "manufacturing", etc.)
	return(d)

def add_ungc_table():
	''' Adds the UNGC participants to a database, using a new table called 'active' '''
	# Open a pool manager object; create a socket requiring certificates
	http = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where())

	# First half of URL of search page of participants
	BASE_URL = "https://www.unglobalcompact.org/what-is-gc/participants/search?page="

	# Root page of UNGC, need for links to non-communicating and delisted entities
	UNGC_URL = "https://www.unglobalcompact.org"
	
	# create a new table with columns called name, type, sector, country, and date
	# Fill table with members of UNGC
	# Can add fields to active, noncomm or delisted by looking at status
	
	database = db()
	
	
	fields = ("name", "org_type", "sector", "country", "global_compact_status", "date_joined", "date_due", "employees", "ownership")
	database.execute('''drop table if exists UNGC;''')
	database.execute("CREATE TABLE UNGC (%s varchar(250), %s varchar(150), %s varchar(150), %s varchar(150), %s varchar(150), %s date, %s date, %s int, %s varchar(150));" % fields)
	# The half of active link after page number
	THE_REST = 	"&search[keywords]=&search[per_page]=50&search[sort_direction]=asc&search[sort_field]=&utf8="
	
	# Is there a way to know how many pages without going to site?
	# Maybe do while loop, checking for 50 things? Probably not worth it, but could be more elegant
	
	for i in range(444): #444 as of 7 Aug 2016
	
		# observe which page we're parsing
		print(i)
		
		# get data from ith page
		soup = data_getter(BASE_URL + str(i+1) + THE_REST)
		
		# get name tags, for links are stored there
		nf = soup.findAll("th", "name")
		
		# build list of links to get important dates, # employees, etc.
		links = [UNGC_URL + th.a["href"] for th in nf[1:]]
		
		# the list of dates for those delistings
		
		for link in links:
			data = ()
			d = scrape_data(link)
			
			# make new tuple of dictionary values
			# Do we really need a dictionary here? should be able to use a list so we don't have to build anything...
			for f in fields:
				data += (d[f], )
			
			#  ('name', 'org_type', 'sector', 'country', 'global_compact_status', 'date_joined', 'date_due', 'employees', 'ownership')
			# postgres wasn't accepting the string unless it was done in 2 pieces, parentheses maybe?
			cmd0 = "INSERT INTO UNGC (%s, %s, %s, %s, %s, %s, %s, %s, %s) " % fields
			cmd1 = "VALUES (%r, %r, %r, %r, %r, %r, %r, %s, %r)" % data
			cmd = cmd0 + cmd1	
			#cmd = cmd.replace('"', "'")	INSERT INTO UNGC SELECT '{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}' WHERE not EXISTS (select name from UNGC where name = '{0}');", row
			# Add to our db:
			try:
				database.execute(cmd)
			except psycopg2.ProgrammingError: # SQL differentiates between " and '
				return(1)
		
		# make sure that we're getting the same number of each of these; names had same tag in headings and content of table
		# print(len(names), len(types), len(sectors), len(countries), len(dates))
		# print(names[0], types[0], sectors[0], countries[0], dates[0])
		

		# Save db
		database.commit()
		database.close()

def add_worldbank_table():
	
	database = db()
	
	fields = ("country", "ind_code", "year", "val")
	database.execute('''drop table if exists WGI;''')

	database.execute("CREATE TABLE WGI (%s varchar(250), %s varchar(150), %s int, %s float);" % fields)
	with open("./WGI_Data.txt", 'r') as f:
		first = f.readline().split('\t')
		print(first, first[3:])
		for line in f:
			# tab delimited is as close as we can get to ok
			l = line.split('\t')
			for i, year in enumerate(first[3:]):
				# dammit commas and spaces. WHY DO YOU PUT COMMAS IN A COUNTRY NAME IN A CSV
				if year == '2014\n':
					year = '2014'
					try: # popping \n
						l[i+3] = l[i+3].split()[0]
					# If there is only a \n (no value for american samoa)
					except IndexError:
						l[i+3] = ''
				l[0] = fix(l[0])
				entry = (l[0], l[2], year, l[i+3])
				if entry[3] != '':
					cmd0 = "INSERT INTO WGI (%s, %s, %s, %s) " % fields
					cmd1 = "VALUES (%r, %r, %r, %r);" % entry
					cmd = cmd0 + cmd1	
					#print(cmd)
					# Add to our db:
					database.execute(cmd)	

	database.commit()
	database.close()
	return(0)
	
#add_worldbank_table()
def add_CPI_table():
	''' Adds CPI data from Transparency International. Not country rank though, not really useful for anything '''
	# CPI_Final has the CPI data from TI, with 0 instead of blanks, 
	# and countries removed if they have data for fewer than 15 years b/t 1995 and 2015.
	
	fields = ("country", "year", "val")
	database = db()
	database.execute('drop table if exists CPI;')
	# we just make year int because m/d doesn't matter
	
	database.execute("CREATE TABLE CPI (%s varchar(250), %s int, %s float);" % fields)
	
	
	def is_number(s):
		''' is s a number? needed for line_fix '''
		try:
			float(s)
			return True
		except ValueError:
			return False

	def line_fix(line):
		''' dammit costa rica!
		necessary for countries with multiple words '''
		l = line.split('\t')
		i = 0
		c = ""
		while is_number(l[i]) is False:
			c += l[i]
			i += 1
		c = "".join([ch for ch in c if ch not in string.punctuation])
		c = c.lower()
		return([c] + l[i:])
	
	with open("./CPI_Final.txt", 'r') as f:
		years = f.readline().split()
		for line in f:
			# clean the line; we want [country, 1995_val, 1996_val, etc] and not [cou, ntry, etc]
			l = line_fix(line)

			country = l[0]
			
			# because the split('\t') leaves \n on the last one...
			l[-1] = l[-1].split()[0]
			
			for i in range(1, len(l)):
				# we only want to add table for years with values
				if l[i] != '0':
					data = (country, years[i-1], l[i])
				
					cmd0 = "INSERT INTO CPI (%s, %s, %s) " % fields
					cmd1 = "VALUES (%r, %r, %r);" % data
					cmd = cmd0 + cmd1	
					# Add to our db:
					database.execute(cmd)

	database.commit()
	database.close()

def count_by_years_table():
	
	# make a list of countries in the UNGC list
	clist = []
	# Fill cursor buffer
	database = db()
	database.query('select distinct country from ungc order by country;')
	# dump cursor buffer into list

	for line in database.query_results:
		# country is a tuple, like ('country', ) so it needs the index
		#print(line[0])
		clist.append(line[0])
		
	# let's just start a new table
	database.execute('drop table if exists BY_COUNTRY;')
	database.execute("CREATE TABLE BY_COUNTRY (Country VARCHAR(250), Year INT, Firms INT, Sectors INT, Types INT, CPI INT);")


	start = timer()

	print('before def')
	def ungc_total_count(database, year, cry):
		'''Returns query '''
		st = "SELECT count(name), count(distinct sector), count(distinct org_type) from UNGC where date_joined < '%s' and date_due >= '%s' and country='%s';" % (year, year+10000, cry)
		database.query(st)
		return(database.query_results[0])
	print('after 1st def')
	def get_cpi(database, yr, cry):
		year = str(yr)[:4]
		# like works for CPI, let's hope world bank follows
		st = "SELECT val from CPI where year='%s' and country ilike('%s');" % (year, cry)
		database.query(st)
		if len(database.query_results) == 0:
			#print(cry)
			return(False)
		else:
			return(database.query_results[0])

	
	print(len(clist))
	for j in range(len(clist)):
		cry = clist[j]
		# ISO standard date format
		yr = 19950101
		for i in range(1,22):
			#print(yr)
			cpi_counts = get_cpi(database, yr, cry)
			# indexed because it's one tuple in a list
			ungc_counts = ungc_total_count(database, yr, cry)
			if cpi_counts is not False:
				year = int(str(yr)[:4])
				st = (cry, year, ungc_counts[0], ungc_counts[1], ungc_counts[2], cpi_counts[0])
				print(st)
			yr = yr + 10000

	end = timer()

	print(end - start)

#count_by_years_table()
	
#add_CPI_table()
#def get_category_links(section_url):


ungc_db = db.db()
st = "SELECT count(name), count(distinct sector), count(distinct org_type) from UNGC where date_joined < '%s' and date_due >= '%s' and country='%s' limit 20;" % (20100101, 20110101, 'brazil')
ungc_db.query(st)

