import mysql.connector


def get_cursor():
	mydb = mysql.connector.connect(
		host="localhost",
		user="root",
		password=""
	)

	return mydb.cursor()


def execute_query(sql, params=None):
	mydb = mysql.connector.connect(
		host="localhost",
		user="root",
		password="",
		database="tcc_render"
	)
	cursor = mydb.cursor(dictionary=True)
	cursor.execute(sql, params)
	result = cursor.fetchall()
	mydb.commit()

	return result


def get_list(sql, params=None):
	mydb = mysql.connector.connect(
		host="localhost",
		user="root",
		password="",
		database="tcc_render"
	)
	cursor = mydb.cursor(dictionary=True)
	cursor.execute(sql, params)

	return cursor.fetchall()


def add(sql, params):
	mydb = mysql.connector.connect(
		host="localhost",
		user="root",
		password="",
		database="tcc_render"
	)
	cursor = mydb.cursor()
	cursor.execute(sql, params)
	mydb.commit()

	return cursor.lastrowid
