from django.conf import settings
import MySQLdb

def sphinxql_query(query):
	db = MySQLdb.connect(host=settings.SPHINXQL_HOST, port=settings.SPHINXQL_PORT)
	cursor = db.cursor()
	return cursor.execute(query) # returns rows_affected