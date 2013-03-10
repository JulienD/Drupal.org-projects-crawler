# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import MySQLdb

from modules.items import Module
from modules.settings import MYSQL

from scrapy.conf import settings

class SQLStorePipeline(object):

	def __init__(self):
		self.conn = MySQLdb.connect(user=MYSQL['user'], passwd=MYSQL['password'], db=MYSQL['dbname'], host=MYSQL['host'], charset = "utf8", use_unicode = True)
		self.cursor =  self.conn.cursor()
		self.cursor.execute("""CREATE TABLE IF NOT EXISTS `modules` (
			  `id` int(11) NOT NULL AUTO_INCREMENT,
			  `name` varchar(255) NOT NULL,
			  `title` varchar(255) NOT NULL,
			  `project_url` tinytext NOT NULL,
			  `git_url` tinytext NOT NULL,
			  `version` varchar(10) NOT NULL,
			  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
			  PRIMARY KEY (`id`),
			  UNIQUE KEY `name` (`name`)
			) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=51 ;""")
		self.conn.commit()

	def process_item(self, item, spider):
		try:
			self.cursor.execute("""INSERT INTO modules (name, title, project_url, git_url, version) VALUES (%s, %s, %s, %s, %s)""",
				(item['name'].encode('utf-8', 'ignore'),
				item['title'].encode('utf-8', 'ignore'),
				item['project_url'].encode('utf-8', 'ignore'),
				item['git_url'],
				item['version'].encode('utf-8', 'ignore'),
				))
			self.conn.commit()

		except MySQLdb.Error, e:
			print ("MySQL Error -------------------------------------------------------")
			print (e)
			print ("-------------------------------------------------------------------")

		return item
