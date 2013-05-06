import MySQLdb
import time
from modules.items import Information, Statistic, Releases, Release
from modules.settings import MYSQL
from scrapy.conf import settings

from datetime import datetime

class SQLStorePipeline(object):

	request_time = ''

	def __init__(self):
		# Connect to the database.
		try:
			self.conn = MySQLdb.connect(user=MYSQL['user'],	passwd=MYSQL['password'], db=MYSQL['dbname'], host=MYSQL['host'],	charset = "utf8",	use_unicode = True)
		except Exception, error:
			print 'Unable to connect to the database'
			print 'Error: %s' % (error)
		else:
			self.cursor = self.conn.cursor()

		self.request_time = datetime.now()

	def process_item(self, item, spider):
		if isinstance(item, Information):
			return self.storeProjectInformation(item, spider)

		elif isinstance(item, Statistic):
			return self.storeProjectStatistics(item, spider)

		elif isinstance(item, Releases):
			return self.storeProjectReleases(item, spider)


	def storeProjectInformation(self, item, spider):
		try:
			self.cursor.execute("""INSERT INTO projects (project_name, project_title, project_url, project_git_url, project_type, created, updated) VALUES (%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE updated = %s """,
				(item['project_name'],
				item['project_title'],
				item['project_url'],
				item['project_git_url'],
				item['project_type'].lower(),
				self.request_time,
				self.request_time,
				self.request_time)
			)
			self.conn.commit()
		except MySQLdb.Error, e:
			print ('Unable to save the projet %s') % (item['project_name'])
			print (' >> %s') % (e)


	def storeProjectStatistics(self, item, spider):
		try:
			self.cursor.execute("""SELECT id FROM projects WHERE project_name = %s;""", (item['project_name']))
			project = self.cursor.fetchone()
			print ('%s') % (item['project_name'])
			if project:
				self.cursor.execute("""INSERT INTO projects_statistics (project_id, project_name, opened_issues, total_issues, opened_bugs, total_bugs, downloads, installs, created) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
					(project[0],
					item.get('project_name'),
					self.getInt(item, 'opened_issues'),
					self.getInt(item, 'total_issues'),
					self.getInt(item, 'opened_bugs'),
					self.getInt(item, 'total_bugs'),
					self.getInt(item, 'downloads'),
					self.getInt(item, 'installs'),
					self.request_time)
				)
				self.conn.commit()
		except MySQLdb.Error, e:
			print ('Unable to save the projet %s') % (item['project_name'])
			print (' >> %s') % (e)


	def storeProjectReleases(self, item, spider):
		try:
			self.cursor.execute("""SELECT id FROM projects WHERE project_name = %s;""", (item['project_name']))
			print ('%s') % (item['project_name'])
			project = self.cursor.fetchone()
			print project
			project_id = project[0]
			if project:
				for release in item.get('releases'):
					self.cursor.execute("""INSERT INTO projects_releases (project_id, release_name, release_version, release_tag, release_date, version_major, version_patch, version_extra, created, updated) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE updated = %s """,
						(project[0],
						release.get('release_name'),
						release.get('release_version'),
						release.get('release_tag'),
						datetime.fromtimestamp(float(release.get('release_date'))),
						int(release.get('version_major', 0)),
						int(release.get('version_patch', 0)),
						release.get('version_extra'),
						self.request_time,
						self.request_time,
						self.request_time)
					)
					self.conn.commit()
		except MySQLdb.Error, e:
			print ('Unable to save the projet %s') % (item['project_name'])
			print (' >> %s') % (e)


	def getInt(self, item, name):
		value = item.get(name)
		if value:
			if value.isnumeric() == True:
				return value
			else:
				# Remove the comma in case the number is higher than 999.
				value = value.replace(',', '')
				# Force the returned value to be an int.
				return int(value)
		else:
			return 0
