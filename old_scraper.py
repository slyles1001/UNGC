#Seth Lyles
#2016 June 22

from bs4 import BeautifulSoup
import urllib3, certifi, psycopg2

# Open a pool manager object; create a socket requiring certificates
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

# Use the try if we might not connect to the db
#try:

# db login info
connect_str = "dbname='NetFinal' user='ducttapecreator' host='localhost' " #+ \
#			  "password='OLIVIA'"

# use our connection values to establish a connection
conn = psycopg2.connect(connect_str)
# create a psycopg2 cursor that can execute queries
cursor = conn.cursor()

# First half of URL of search page of participants
BASE_URL = 'https://www.unglobalcompact.org/what-is-gc/participants/search?page='

# Root page of UNGC, need for links to non-communicating and delisted entities
UNGC_URL = 'https://www.unglobalcompact.org'


def data_getter(url):
	''' Returns the page data from URL '''
	ld = http.request('GET', url)
	sp = BeautifulSoup(ld.data, "lxml")
	return(sp)

def get_leave_date(url):
	''' Finds the date that the entity became delisted at URL '''
	sp = data_getter(url)
	
	# Format of text we're searching:
	#<div class='company-information-cop-due'><strong>Delisted on:</strong> <time>2016-02-02</time></div>
	ldtext = sp.find('div',  {'class':'company-information-cop-due'})
	othertext = sp.find('div', {'class':'company-information-overview'})
	other_list = othertext.findAll('dd')
  # 		<div class='column company-information-overview'>
  #           <h2>Overview</h2>
  # 
  #           <dl>
  #               <dt>Country:</dt>
  #               <dd>United Arab Emirates</dd>
  # 
  #               <dt>Org. Type:</dt>
  #               <dd>SME</dd>
  # 
  #               <dt>Sector:</dt>
  #               <dd>Travel &amp; Leisure</dd>
  # 
  #             <dt>Global Compact Status:</dt>
  #             <dd>Delisted</dd>
  # 
  #               <dt>Reason for Delisting:</dt>
  #               <dd>Other reason related to the Integrity Measures</dd>
  # 
  #               <dt>Employees:</dt>
  #               <dd>20</dd>
  # 
  #               <dt>Ownership:</dt>
  #               <dd>Privately Held</dd>
  # 
  #           </dl>	
	return(ldtext.time.string)

def add_active():
	''' Adds the UNGC participants to a database, using a new table called 'active' '''
	# create a new table with columns called name, type, sector, country, and date
	# Fill table with the active members of UNGC
	cursor.execute("""CREATE TABLE active (name char(150), type char(150), sector char(150), country char(150), date date);""")
	
	# The half of active link after page number
	THE_REST_ACTIVE = 	'&search[keywords]=&search[per_page]=50&search[reporting_status][]=active&search[sort_direction]=asc&search[sort_field]=&utf8='
	
	# Is there a way to know how many pages without going to site?
	# Maybe do while loop, checking for 50 things? Probably not worth it, but could be more elegant
	for i in range(215):
	
		# observe which page we're parsing
		print(i)
		
		# get data from ith page
		soup = data_getter(BASE_URL + str(i+1) + THE_REST_ACTIVE)

		#Name    Type    Sector    Country	date

		# <th class='name'><a href="/what-is-gc/participants/71191-The-Luxury-Global">The Luxury Global</a></th>
        # <td class='type'>Small or Medium-sized Enterprise</td>
        # <td class='sector'>Travel &amp; Leisure</td>
        # <td class='country'>United Arab Emirates</td>
        # <td class='joined-on'>2015-12-01</td>
        
		names = [th.string for th in soup.findAll("th", 'name')][1:]
		types = [td.string for td in soup.findAll('td', 'type')]
		sectors = [td.string for td in soup.findAll('td', 'sector')]
		countries = [td.string for td in soup.findAll('td', 'country')]
		dates = [td.string for td in soup.findAll('td', 'joined-on')]
		
		# make sure that we're getting the same number of each of these; names had same tag in headings and content of table
		# print(len(names), len(types), len(sectors), len(countries), len(dates))
		# print(names[0], types[0], sectors[0], countries[0], dates[0])
		
		# Add to our db:
		for j in range(len(names)):
			cursor.execute("""INSERT INTO active (name, type, sector, country, date)
								VALUES (%s, %s, %s, %s, %s)""",
								(names[j], types[j], sectors[j], countries[j], dates[j]))
								
		# Save db
		conn.commit()
	
def add_delisted():
	''' Adds the UNGC participants to a database, using a new table called 'active' '''
	cursor.execute("""CREATE TABLE delisted (name char(150), type char(150), sector char(150), country char(150), join_date date, delist_date date, reason char(200), size int, ownership char(50));""")
	THE_REST_DELISTED = '&search[keywords]=&search[reporting_status][]=delisted&search[per_page]=50&search[sort_field]=&search[sort_direction]=asc%27'
	for i in range(158): #158 as of june22
		print(i)
		soup = data_getter(BASE_URL + str(i+1) + THE_REST_DELISTED)

		#Name    Type    Sector    Country	Join_date Delist_date
		nf = soup.findAll("th", 'name')
		names = [th.string for th in nf][1:]
		#print(names)
		types = [td.string for td in soup.findAll('td', 'type')]
		sectors = [td.string for td in soup.findAll('td', 'sector')]
		countries = [td.string for td in soup.findAll('td', 'country')]
		dates = [td.string for td in soup.findAll('td', 'joined-on')]
		namelink = soup.find("table", "participants-table")
		
    	#<th class='name'><a href="/what-is-gc/participants/71191-The-Luxury-Global">
		
		# What a BATCH!! There was no href for the first one... was getting Nonetype no subscript error :(
		# skip it; Thanks, slicing!
		# The list of links to find the exit dates of participants
		links = [UNGC_URL + th.a['href'] for th in nf[1:]]
		
		# the list of dates for those delistings
		leavedates = []
		for link in links:
			leavedates.append(get_leave_date(link))
			

		
		#print(len(names), len(types), len(sectors), len(countries), len(dates), len(links))
		#print(names[0], types[0], sectors[0], countries[0], dates[0], links[0])
		for j in range(len(names)):
			cursor.execute("""INSERT INTO delisted (name, type, sector, country, join_date, delist_date)
								VALUES (%s, %s, %s, %s, %s, %s)""",
								(names[j], types[j], sectors[j], countries[j], dates[j], leavedates[j]))
		
		conn.commit()
		
def add_noncomm():
	cursor.execute("""CREATE TABLE noncommunicating (name char(150), type char(150), sector char(150), country char(150), join_date date, due_date date);""")
	THE_REST_NONCOMM = '&search[keywords]=&search[reporting_status][]=noncommunicating&search[per_page]=50&search[sort_field]=&search[sort_direction]=asc%27'
	for i in range(96): #96 as of june22
		print(i)
		soup = data_getter(BASE_URL + str(i+1) + THE_REST_NONCOMM)

		#Name    Type    Sector    Country	Join_date due_date
		nf = soup.findAll("th", 'name')
		
		# The list of links to find the exit dates of entities
		links = [UNGC_URL + th.a['href'] for th in nf[1:]]
		
		# the list of dates for those leavings
		leavedates = []
		for j in range(len(links)):
			leavedates.append(get_leave_date(links[j]))
		
		names = [th.string for th in nf][1:]
		
		#print(names)
		types = [td.string for td in soup.findAll('td', 'type')]
		sectors = [td.string for td in soup.findAll('td', 'sector')]
		countries = [td.string for td in soup.findAll('td', 'country')]
		dates = [td.string for td in soup.findAll('td', 'joined-on')]
		namelink = soup.find("table", "participants-table")

		links = [UNGC_URL + th.a['href'] for th in nf[1:]]
		
		# the list of dates when COP was due
		duedates = []
		for link in links:
			duedates.append(get_leave_date(link))
			
		print(len(names), len(types), len(sectors), len(countries), len(dates), len(links))
		print(names[0], types[0], sectors[0], countries[0], dates[0], links[0])
		for j in range(len(names)):
			cursor.execute("""INSERT INTO noncommunicating (name, type, sector, country, join_date, due_date)
								VALUES (%s, %s, %s, %s, %s, %s)""",
								(names[j], types[j], sectors[j], countries[j], dates[j], duedates[j]))
		
		conn.commit()		

add_active()

#add_delisted()
#cursor.execute("""SELECT delist_date from delisted""")
#cs = cursor.fetchall()
#for c in cs:
#	print(c)

cursor.close()
conn.close()

#except Exception as e:
#    print("Uh oh, can't connect. Invalid dbname, user or password?")
#    print(e)





#def get_category_links(section_url):
    



