import MySQLdb
import time

from modules.items import Project, Information, Statistic, Release

from modules.settings import MYSQL
from scrapy.conf import settings

from datetime import datetime

class SQLStorePipeline(object):
    request_time = ''

    project_id = ''

    def __init__(self):
        # Connect to the database.
        try:
            self.conn = MySQLdb.connect(user=MYSQL['user'], passwd=MYSQL['password'], db=MYSQL['dbname'],
                                        host=MYSQL['host'], charset="utf8", use_unicode=True)
        except Exception, error:
            print 'Unable to connect to the database'
            print 'Error: %s' % (error)
        else:
            self.cursor = self.conn.cursor()

        self.request_time = datetime.now()

    def process_item(self, item, spider):

        #print '+ + + + + + + + + '
        print ">>>>> Saving : %s" % (item['name'])
        #print '- - - - - - - - - '

        # Checks the instance of the received item.
        if isinstance(item, Project):
            # Stores project information.
            self.storeProjectInformation(item, spider)

            # Gets the id for the saved project.
            self.cursor.execute("""SELECT id FROM projects WHERE name = %s""", ([item['name']]))
            self.project_id = self.cursor.fetchone()
            self.project_id = self.project_id[0]

            # Saves project versions.
            self.storeProjectVersion(item, spider)

            # Saves project releases.
            self.storeProjectReleases(item, spider)

            # Saves project statistics.
            self.storeProjectStatistics(item, spider)
            return

    '''
        Saves or updates project information.
    '''

    def storeProjectInformation(self, item, spider):
        try:
            self.cursor.execute("""INSERT INTO projects (name, title, url, git_url,
														 last_commit, type, created, updated)
									VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
									ON DUPLICATE KEY UPDATE name = %s, title = %s, url = %s, git_url = %s,
															last_commit = %s, type = %s, updated = %s """,
                                (item['name'],
                                 item['information']['title'],
                                 item['information']['url'],
                                 item['information']['git_url'],
                                 datetime.strptime(item['information']['last_commit'], "%B %d, %Y %H:%M").strftime(
                                     "%Y-%m-%dT%H:%M:%S"),
                                 item['information']['type'].lower(),
                                 self.request_time,
                                 self.request_time,
                                 item['name'],
                                 item['information']['title'],
                                 item['information']['url'],
                                 item['information']['git_url'],
                                 datetime.strptime(item['information']['last_commit'], "%B %d, %Y %H:%M").strftime(
                                     "%Y-%m-%dT%H:%M:%S"),
                                 item['information']['type'].lower(),
                                 self.request_time)
            )
            self.conn.commit()
        except MySQLdb.Error, e:
            print ('Unable to save the projet %s') % (item['name'])
            print (' >> %s') % (e)


    '''
        Saves project versions
    '''

    def storeProjectVersion(self, item, spider):
        for version in item['information']['supported_majors'].split(','):
            try:
                self.cursor.execute("""INSERT INTO versions (project_id, api_version, recommended_major,
															  supported_majors, default_major) 
									VALUES (%s, %s, %s, %s, %s)""",
                                    (int(self.project_id),
                                     item['information']['api_version'],
                                     item['information']['recommended_major'],
                                     version,
                                     item['information']['default_major'])
                )
                self.conn.commit()
            except MySQLdb.Error, e:
                print ('Unable to save versions for the projet %s') % (item['name'])
                print (' >> %s') % (e)

    '''
        Save releases for a project.
    '''

    def storeProjectReleases(self, item, spider):
        try:
            for release in item['releases']:
                self.cursor.execute(
                    """INSERT INTO releases (project_id, name, version, tag, date, version_major, version_patch, version_extra) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                    (int(self.project_id),
                     release.get('name'),
                     release.get('version'),
                     release.get('tag'),
                     datetime.fromtimestamp(float(release.get('date'))),
                     release.get('version_major'),
                     release.get('version_patch'),
                     release.get('version_extra'))
                )
                self.conn.commit()
                print ('Save release for the projet %s') % (self.project_id)
            #print 'data %s' % (item)
        except MySQLdb.Error, e:
            print ('Unable to save release for the projet %s') % (item['name'])
            print (' >> %s') % (e)

    '''
        Saves statistics given a project
            - number of downloads and installs
            - total and opened bugs
            - total and opened issues
    '''

    def storeProjectStatistics(self, item, spider):
        try:
            self.cursor.execute(
                """INSERT INTO statistics (project_id, opened_issues, total_issues, opened_bugs, total_bugs, downloads, installs, created) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                (int(self.project_id),
                 self.getInt(item['statistics'], 'opened_issues'),
                 self.getInt(item['statistics'], 'total_issues'),
                 self.getInt(item['statistics'], 'opened_bugs'),
                 self.getInt(item['statistics'], 'total_bugs'),
                 self.getInt(item['statistics'], 'downloads'),
                 self.getInt(item['statistics'], 'installs'),
                 self.request_time)
            )
            self.conn.commit()
        except MySQLdb.Error, e:
            print ('Unable to save statistics for the projet %s') % (item['name'])
            print (' >> %s') % (e)

    '''
    Helper function to convert a ...
    '''

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
