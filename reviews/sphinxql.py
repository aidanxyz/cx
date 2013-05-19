from django.conf import settings
import MySQLdb
from contextlib import closing

"""
For "insert" and "delete" statements
"""
def sphinxql_query(query):
	connection = MySQLdb.connect(host=settings.SPHINXQL_HOST, port=settings.SPHINXQL_PORT)
	cursor = connection.cursor()
	numrows_affected = cursor.execute(query)
	cursor.close()
	connection.close()
	return numrows_affected