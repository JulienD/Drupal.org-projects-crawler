from scrapy.contrib.spiders import XMLFeedSpider
from scrapy.selector import Selector
from scrapy.http import Request
from subprocess import call
from modules.items import Project, Information, Statistic, Release


class ModuleXml(XMLFeedSpider):
    name = 'ModulesXml'

    allowed_domains = ["drupal.org"]
    start_urls = ["http://updates.drupal.org/release-history/project-list/all/7"]
    #start_urls = ["http://drupal-commerce.local/drupal-project-release-7.xml"]

    iterator = 'iternodes'
    itertag = 'projects'

    def __init__(self, version='7'):
        self.version = '%s.x' % (version)
        

    """
      Main parser.
    """
    def parse(self, response):
        # Parses the response.
        sel = Selector(response)
        # Extract all the projects.
        projects = sel.xpath('/projects/project')
        projects.extract()

        for index, node in enumerate(projects):

            # Initialize a project.
            project = Project()
            project['name'] = node.xpath('short_name/text()').extract()[0]

            # Sandboxes are named with numeric values and doesn't have
            # information available in projects xml feed.
            if node.xpath('short_name/text()').extract()[0].isnumeric() == True:
                # TODO : find how to extract information for sandboxes. We need
                # to store them at least.
                pass
            # Real projects have real names.
            else:
                project['information'] = Information()
                project['statistics'] = Statistic()
                project['releases'] = []

                # Gets information about the project.
                url = "http://updates.drupal.org/release-history/%s/%s" % (project['name'], self.version)
                yield Request(url=url, meta={'project': project},
                              callback=self.parse_project_xml)


    """
      Helper function to parse project xml feed.
    """
    def parse_project_xml(self, response):

        # Parses the response.
        sel = Selector(response)
        # Gets the project item.
        project = response.meta['project']

        if not (sel.xpath("title/text()").extract()):
            return
        else:
            # Title.
            project['information']['title'] = sel.xpath("title/text()").extract()[0]
            project['information']['type'] = '';
            # Type - extracts all the the first term to gets the project type - module | theme | distribution.
            for term in sel.xpath('terms/term'):
                if term.xpath('name/text()').extract()[0] == 'Projects':
                    # Gets the project type from the first term.
                    project['information']['type'] = term.xpath('value/text()').extract()[0]
                    break

            # Url.
            project['information']['url'] = sel.xpath("link/text()").extract()[0]

            # Git url.
            project['information']['git_url'] = "http://git.drupal.org/project/%s.git" % (project['name'])

            # Api version.
            project['information']['api_version'] = sel.xpath('api_version/text()').extract()[0]

            # Recommended major version.
            if sel.xpath("recommended_major/text()").extract():
                project['information']['recommended_major'] = sel.xpath("recommended_major/text()").extract()[0]
            else:
                project['information']['recommended_major'] = ''

            # Supported major version.
            if sel.xpath("supported_majors/text()").extract():
                project['information']['supported_majors'] = sel.xpath("supported_majors/text()").extract()[0]
            else:
                project['information']['supported_majors'] = ''

            # Default major version.
            if sel.xpath("default_major/text()").extract():
                project['information']['default_major'] = sel.xpath("default_major/text()").extract()[0]
            else:
                project['information']['default_major'] = ''

            #
            for version in sel.xpath('releases/release'):
                release = Release()
                #
                if version.xpath('name/text()').extract():
                    release['name'] = version.xpath('name/text()').extract()[0]
                #
                if version.xpath('version/text()').extract():
                    release['version'] = version.xpath('version/text()').extract()[0]
                #
                if version.xpath('tag/text()').extract():
                    release['tag'] = version.xpath('tag/text()').extract()[0]
                #
                if version.xpath('date/text()').extract():
                    release['date'] = version.xpath('date/text()').extract()[0]
                #
                if version.xpath('version_major/text()').extract():
                    release['version_major'] = version.xpath('version_major/text()').extract()[0]
                #
                if version.xpath('version_patch/text()').extract():
                    release['version_patch'] = version.xpath('version_patch/text()').extract()[0]
                #
                if version.xpath('version_extra/text()').extract():
                    release['version_extra'] = version.xpath('version_extra/text()').extract()[0]

                project['releases'].append(release)

            url = "https://drupal.org/project/%s" % (project['name'])
            yield Request(url=url, meta={'project': project},
                          callback=self.parse_project_page)



    """
      Project page parser.
    """
    def parse_project_page(self, response):
        sel = Selector(response)
        project = response.meta['project']

        # Issues
        issues = sel.xpath('//div[@class="issue-cockpit-All"]/div[@class="issue-cockpit-totals"]/a/text()')
        if issues:
            project['statistics']['opened_issues'] = issues.extract()[0].split(' ')[0]
            project['statistics']['total_issues'] = issues.extract()[1].split(' ')[0]

        # Bugs.
        bugs = sel.xpath('//div[@class="issue-cockpit-1"]/div[@class="issue-cockpit-totals"]/a/text()')
        if bugs:
            project['statistics']['opened_bugs'] = bugs.extract()[0].split(' ')[0]
            project['statistics']['total_bugs'] = bugs.extract()[1].split(' ')[0]

        # Downloads and Installations
        for stats in sel.xpath('//div[contains(@class,"project-info")]/ul/li'):
            if stats.xpath('text()').extract()[0].startswith('Downloads'):
                project['statistics']['downloads'] = stats.xpath('text()').extract()[0].split(' ')[1]

            if stats.xpath('text()').extract()[0].startswith('Reported installs'):
                project['statistics']['installs'] = stats.xpath('strong/text()').extract()[0]


        '''
        # Maintainers
        print '>> maintainers'
        for maintainer in sel.xpath('//div[contains(@id, "block-versioncontrol-project-project-maintainers")]/div/div/div/ul/li/div/a'):
            uid = maintainer.select('@href').extract()[0]
            project['releases'].append(uid)
        '''

        # Continue to get commits information.
        url = "https://drupal.org%s" % (sel.xpath('//div[@id="project-commits"]/a/@href').extract()[0])
        yield Request(url=url, meta={'project': project},
                      callback=self.parse_project_commit_page)


    """
      Project commit page parser.
    """
    def parse_project_commit_page(self, response):
        sel = Selector(response)
        project = response.meta['project']

        project['information']['last_commit'] = \
        sel.xpath("//*[contains(concat(' ', @class, ' '), ' views-row-1 ')]/div/span/div/h3/a/text()").extract()[0]

        return project
