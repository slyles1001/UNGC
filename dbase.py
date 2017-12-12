import urllib3, certifi, psycopg2, string


class db:
	'''Class containing the database connection
	Makes use of psycopg2 cleaner and easier
	No need for global connection to DB'''
	def __init__(self, connect_str = "dbname='ungc_test' user='ducttapecreator' host='localhost'"):
		'''Make new db object, consolidating psycopg2.connect and psycopg2.connect.cursor into one thing'''
		# Use the try if we might not connect to the db
		try:
			# db login info
			# may want to pass this into init later, if we have multiple dbs
			

			# use our connection values to establish a connection
			self.conn = psycopg2.connect(connect_str)
			self.cursor = self.conn.cursor()
			# create a psycopg2 cursor that can execute queries
			#return(conn)
		except Exception as e:
			print("Can't connect. Invalid dbname, user or password?")
			print(e)

	def is_closed(self):
		if self.cursor.closed:
			print("Please create a new db object.")
			return(True)
		else:
			return(False)

	def commit(self):
		#breififying
		if not self.is_closed():
			self.conn.commit()
	
	def execute(self, exec_string):
		#breififying
		if not self.is_closed():
			self.cursor.execute(exec_string)

	def query(self, exec_string):
		'''distinguish from execute by returning a list instead of the weird buffer thing'''		
		if not self.is_closed():
			self.execute(exec_string)
			self.query_results = self.cursor.fetchall()
		
	def close(self):
		# May not be the best way to do this, but is_closed() should protect from error.
		if not self.is_closed():
			self.cursor.close()
			self.conn.close()
	
	def __str__(self):
		try:
			return str(self.query_results)
		except AttributeError:
			print('Please query the DB first')

