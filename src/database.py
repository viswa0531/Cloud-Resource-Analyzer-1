import os
import settings
import psycopg2
import pandas as pd
import pandas.io.sql as sqlio

class DatabaseError(Exception):
	""" This will be raised when there is any db related error"""

class PostgresDb(object):
	"""

	"""

	def __init__(self, hostname=settings.PROMQL_HOSTNAME, port=settings.PROMQL_PORT, username=settings.PROMQL_USERNAME, password=settings.PROMQLDB_PASSWORD,
				database=settings.PROMQL_DB_NAME):
		self.host = hostname
		self.port = port
		self.username = username
		self.password = password
		self.database = database
		self.connection = psycopg2.connect(user = self.username, password=self.password, host=self.host, port=self.port, database=self.database)
		self.session = self.connection.cursor()

	def db_connect(self):
		#self.connection = psycopg2.connect(user = self.username, password=self.password, host=self.host, port=self.port, database=self.database)
		#self.session = self.connection.cursor
		#return self.session
		pass

	def db_execute(self, query):
		self.session.execute(query)

	def db_fetch(self):
		records = self.session.fetchall()
		#read each data record in a for loop 
		return records

	def db_getPDFrame(self, query):
		""" Executes the query and return the data in panda frame"""
		dataframe = sqlio.read_sql_query(query, self.connection)
		return dataframe.dropna()

	def db_close(self):
		self.session.close()	
		

system = "SELECT time, value AS \"node_cpu_seconds_total\" FROM metrics WHERE labels->>'cpu' = '0' and labels->>'mode' = 'system'  AND name='node_cpu_seconds_total' ORDER BY time"

irq = "SELECT time, value AS \"node_cpu_seconds_total\" FROM metrics WHERE labels->>'cpu' = '0' and labels->>'mode' = 'irq'  AND name='node_cpu_seconds_total' ORDER BY time"
	
iowait = "SELECT time, value AS \"node_cpu_seconds_total\" FROM metrics WHERE labels->>'cpu' = '0' and labels->>'mode' = 'iowait'  AND name='node_cpu_seconds_total' ORDER BY time"

idle = "SELECT time, value AS \"node_cpu_seconds_total\" FROM metrics WHERE labels->>'cpu' = '0' and labels->>'mode' = 'idle'  AND name='node_cpu_seconds_total' ORDER BY time"

nice = "SELECT time, value AS \"node_cpu_seconds_total\" FROM metrics WHERE labels->>'cpu' = '0' and labels->>'mode' = 'nice'  AND name='node_cpu_seconds_total' ORDER BY time"

softirq = "SELECT time, value AS \"node_cpu_seconds_total\" FROM metrics WHERE labels->>'cpu' = '0' and labels->>'mode' = 'softirq'  AND name='node_cpu_seconds_total' ORDER BY time"

steal = "SELECT time, value AS \"node_cpu_seconds_total\" FROM metrics WHERE labels->>'cpu' = '0' and labels->>'mode' = 'steal'  AND name='node_cpu_seconds_total' ORDER BY time"

user = "SELECT time, value AS \"node_cpu_seconds_total\" FROM metrics WHERE labels->>'cpu' = '0' and labels->>'mode' = 'user'  AND name='node_cpu_seconds_total' ORDER BY time"

def getDatafromDb():
	#Creates a an object
	con = PostgresDb()

	#Executes a query
	#con.db_execute(system)

	#fetch all records
	#records = con.db_fetch()

	#gets data in pandaframes
	sData = con.db_getPDFrame(system)
	uData = con.db_getPDFrame(user)
	iData = con.db_getPDFrame(idle)
	ioData = con.db_getPDFrame(iowait)
	irData = con.db_getPDFrame(irq)
	nData = con.db_getPDFrame(nice)
	siData = con.db_getPDFrame(softirq)
	stData = con.db_getPDFrame(steal)
         
	sframe = pd.DataFrame(data=sData)
	sframe.rename({"node_cpu_seconds_total": "system"}, inplace=True, axis=1)

	uframe = pd.DataFrame(data=uData)
	uframe.rename({"node_cpu_seconds_total": "user"}, inplace=True, axis=1)

	iframe = pd.DataFrame(data=iData)
	iframe.rename({"node_cpu_seconds_total": "idle"}, inplace=True, axis=1)

	ioframe = pd.DataFrame(data=ioData)
	ioframe.rename({"node_cpu_seconds_total": "iowait"}, inplace=True, axis=1)

	irframe = pd.DataFrame(data=irData)
	irframe.rename({"node_cpu_seconds_total": "irq"}, inplace=True, axis=1)

	nframe = pd.DataFrame(data=nData)
	nframe.rename({"node_cpu_seconds_total": "nice"}, inplace=True, axis=1)

	siframe = pd.DataFrame(data=siData)
	siframe.rename({"node_cpu_seconds_total": "softirq"}, inplace=True, axis=1)

	stframe = pd.DataFrame(data=stData)
	stframe.rename({"node_cpu_seconds_total": "steal"}, inplace=True, axis=1)

	print(uframe)
	print(sframe)
	print(ioframe)
	print(iframe)

	print(nframe)
	print(siframe)
	print(stframe)
	print(iframe)

	uframe.reset_index(drop=True, inplace=True)
	sframe.reset_index(drop=True, inplace=True)
	ioframe.reset_index(drop=True, inplace=True)
	irframe.reset_index(drop=True, inplace=True)

	nframe.reset_index(drop=True, inplace=True)
	siframe.reset_index(drop=True, inplace=True)
	stframe.reset_index(drop=True, inplace=True)
	iframe.reset_index(drop=True, inplace=True)
	print("Done Done Done Done Done")
	print("-------------------------------------------")
	cuFrame = uframe[uframe.time.isin(sframe.time)]
	cioFrame = ioframe[ioframe.time.isin(sframe.time)]
	cirFrame = irframe[irframe.time.isin(sframe.time)]
	cnFrame = nframe[nframe.time.isin(sframe.time)]
	csiFrame = siframe[siframe.time.isin(sframe.time)]
	cstFrame = stframe[stframe.time.isin(sframe.time)]
	ciFrame = iframe[iframe.time.isin(sframe.time)]
	print(cuFrame)
	print(cioFrame)	
	print("-------------------------------------------")
	print("End End End End End End")
	#dataframe = pd.concat([sframe, uframe], ignore_index=True)
	#dataframe = pd.concat([sframe, uframe['user'], ioframe['iowait'], irframe['irq'], nframe['nice'], siframe['softirq'], stframe['steal'], iframe['idle']], axis=1, sort=True)
	dataframe = pd.concat([sframe, cuFrame['user'], cioFrame['iowait'], cirFrame['irq'], cnFrame['nice'], csiFrame['softirq'], cstFrame['steal'], ciFrame['idle']], axis=1, sort=True)
	#close the sesssion
	con.db_close()
	return dataframe

def getCpuUtilization(dframe):
	"""
	Get CPU Utilization
	"""
	dframe.dropna()	
	last_idle = 0
	last_total = 0
	cpuUtilPct = []
	colN = getColumnNames(dframe)
	for index, row in dframe.iterrows():
		#print("index: ", index)
		cTotal = cSum(row, colN)
		idle = row['idle']
		#print("**************************")
		#print(cTotal, idle)
		idle_delta, total_delta = idle - last_idle, cTotal - last_total
		last_idle, last_total = idle, cTotal
		CpuUtilization = 100 * (1.0 - idle_delta/total_delta)
		#print(CpuUtilization)
		#print("**************************")
		cpuUtilPct.append(CpuUtilization)
	dframe['CpuUtilization']= cpuUtilPct
	return dframe

	
def getColumnNames(df):
	"""
	 get data frame column names
	"""
	Cname = []
	for col in df.columns:
		Cname.append(col)
	return Cname[1:]

def cSum(rdata, cnames):
	"""
	get the sum of values
	"""
	cTotal = 0.0 
	for cn in (cnames):
		#print(cn, rdata[cn])
		cTotal += rdata[cn]
	#print("cTotal: ", cTotal)
	return cTotal 
	

if __name__ == "__main__":
	dFrame = getDatafromDb()
	print(dFrame)
	df = getCpuUtilization(dFrame)
	print(df)
	"""
	print("==============================")
	print(dFrame['system'][0])
	print("==============================")

	cnames = getColumnNames(dFrame)
	print(cnames)
	print("==============================")
	print(dFrame.loc[0])
	print("==============================")
	ct = cSum(dFrame.loc[0], cnames) 
	print("*******************************")
	print(ct)
	"""

   
