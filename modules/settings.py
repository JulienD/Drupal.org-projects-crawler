# Scrapy settings for drupalmodules project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'modules'
BOT_VERSION = '1.0'

USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

SPIDER_MODULES = ['modules.spiders']
NEWSPIDER_MODULE = 'modules.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'drupalmodules (+http://www.yourdomain.com)'
# Our do-it-all pipeline
ITEM_PIPELINES = [
  'modules.pipelines.SQLStorePipeline'
]

MYSQL = {
	'user':'root',
	'host':'localhost',
	'password':'password',
	'dbname':'drupal_projects'
}