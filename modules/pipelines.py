import MySQLdb
from modules.items import Module
from modules.settings import MYSQL

from scrapy.conf import settings

class SQLStorePipeline(object):

	table_name = 'modules';

	def __init__(self):
		# Connect to the database.
		try:
			self.conn = MySQLdb.connect(user=MYSQL['user'], passwd=MYSQL['password'], db=MYSQL['dbname'], host=MYSQL['host'], charset = "utf8", use_unicode = True)
		except Exception, error:
			print 'Unable to connect to the database'
			print 'Error: %s' % (error)
		else:
			self.cursor =  self.conn.cursor()
			# Test if the table exist or not.
			self.cursor.execute("""SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %s AND table_name = %s;""", (MYSQL['dbname'], self.table_name))
			result = self.cursor.fetchone()
			# Create the table if it has not already been done.
			if (not(result[0] == True)):
				self.createTable();

	def process_item(self, item, spider):
		try:
			self.cursor.execute("""INSERT IGNORE INTO %s (name, title, project_url, git_url, version) VALUES (%%s, %%s, %%s, %%s, %%s)""" % self.table_name,
				(item['name'].encode('utf-8', 'ignore'),
				item['title'].encode('utf-8', 'ignore'),
				item['project_url'].encode('utf-8', 'ignore'),
				item['git_url'],
				item['version'].encode('utf-8', 'ignore'),
			))
			self.conn.commit()
		except MySQLdb.Error, e:
			print ('Unable to save the projet %s') % (item['name'])
			print (' >> %s') % (e)

		return item

	def createTable(self):
		self.cursor.execute("""CREATE TABLE IF NOT EXISTS %s (
			  `id` int(11) NOT NULL AUTO_INCREMENT,
			  `name` varchar(255) NOT NULL,
			  `title` varchar(255) NOT NULL,
			  `project_url` tinytext NOT NULL,
			  `git_url` tinytext NOT NULL,
  			`version` varchar(10) DEFAULT NULL,
  			`exclude` tinyint(1) NOT NULL DEFAULT '0',
			  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
			  PRIMARY KEY (`id`),
			  UNIQUE KEY `name` (`name`)
			);""" % self.table_name)
		self.conn.commit()
