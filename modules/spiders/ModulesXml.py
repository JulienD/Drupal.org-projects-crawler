from scrapy.contrib.spiders import XMLFeedSpider
from scrapy.selector import XmlXPathSelector
from scrapy.http import Request

from subprocess import call

from modules.items import Module

class ModuleXml(XMLFeedSpider):
    name = 'ModulesXml'

    allowed_domains = ["drupal.org"]
    start_urls = ["http://updates.drupal.org/release-history/project-list/all/7"]

    iterator = 'iternodes'
    itertag = 'projects'

    def __init__(self, version = '7'):
        self.version = '%s.x' % (version)

    def parse_node(self, response, node):
        modules = []
        for name in node.select('project/short_name/text()').extract():
            # Only real project as names with caracters, sandboxes used numeric values
            # Exit is the project is a sandbox
            if name.isnumeric() == False:
                project_url = "http://updates.drupal.org/release-history/%s/%s" % (name, self.version)
                modules.append(Request(url=project_url, callback=self.parse_project))
        return modules

    def parse_project(self, response):
            xxs = XmlXPathSelector(response)

            if not (xxs.select('/error/text()').extract()):
                name = xxs.select('short_name/text()').extract()[0]
                if name:
                    item = Module()
                    item['name'] = name
                    item['title'] = xxs.select('title/text()').extract()[0]
                    item['project_url'] = xxs.select('link/text()').extract()[0]
                    item['git_url'] = "http://git.drupal.org/project/%s.git" % (name)
                    item['version'] = xxs.select('default_major/text()').extract()[0]
                    yield item


#scrapy crawl ModulesXml -a version=7