from scrapy.contrib.spiders import XMLFeedSpider
from scrapy.selector import XmlXPathSelector, HtmlXPathSelector
from scrapy.http import Request
from subprocess import call
from modules.items import Information, Statistic, Releases, Release

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
    for project_name in node.select('project/short_name/text()').extract():
      # Sandboxes are nammed with numeric values.
      if project_name.isnumeric() == True:
        pass
      # Real project has real name.
      else:
        project_release_url = "http://updates.drupal.org/release-history/%s/%s" % (project_name, self.version)
        modules.append(Request(url=project_release_url, callback=self.parseProjectInformation, meta={'project_name': project_name}, priority=200))
        modules.append(Request(url=project_release_url, callback=self.parseProjectVersion, meta={'project_name': project_name}, dont_filter=True))
        project_page_url = "http://drupal.org/project/%s" % (project_name)
        modules.append(Request(url=project_page_url, callback=self.parseProjectStatistics, meta={'project_name': project_name}, priority=100))
    return modules


  def parseProjectInformation(self, response):
    xxs = XmlXPathSelector(response)
    # Ensure the project exist and the page don't display an error.
    if not (xxs.select('/error/text()').extract()):
      if xxs.select('short_name/text()').extract():
        info = Information()
        info['project_name'] = response.meta['project_name']
        info['project_title'] = xxs.select("title/text()").extract()[0]
        info['project_url'] = xxs.select("link/text()").extract()[0]
        info['project_git_url'] = "http://git.drupal.org/project/%s.git" % (response.meta['project_name'])

        # Extracts all the terms to gets the project type module/theme
        terms = xxs.select('terms/term')
        info['project_type'] = ''
        for term in terms:
          if term.select('name/text()').extract()[0] == 'Projects':
            # The first value is the project type.
            info['project_type'] = term.select('value/text()').extract()[0]
            break
        yield info


  def parseProjectVersion(self, response):
    xxs = XmlXPathSelector(response)
    # Ensure the project exist and the page don't display an error.
    if not (xxs.select('/error/text()').extract()):
      if xxs.select('short_name/text()').extract():
        releases = Releases()
        releases['project_name'] = response.meta['project_name']
        releases['releases'] = []

        for version in xxs.select('releases/release'):
          release = Release()
          if version.select('name/text()').extract():
            release['release_name'] = version.select('name/text()').extract()[0]
          if version.select('version/text()').extract():
            release['release_version'] = version.select('version/text()').extract()[0]
          if version.select('tag/text()').extract():
            release['release_tag'] = version.select('tag/text()').extract()[0]
          if version.select('version_major/text()').extract():
            release['version_major'] = version.select('version_major/text()').extract()[0]
          if version.select('version_patch/text()').extract():
            release['version_patch'] = version.select('version_patch/text()').extract()[0]
          if version.select('version_extra/text()').extract():
            release['version_extra'] = version.select('version_extra/text()').extract()[0]
          if version.select('date/text()').extract():
            release['release_date'] = version.select('date/text()').extract()[0]
          releases['releases'].append(release)

        yield releases


  def parseProjectStatistics(self, response):
    statictics = Statistic()
    hxs = HtmlXPathSelector(response)

    print response.meta['project_name']

    statictics['project_name'] = response.meta['project_name']

    # Gets the issues report section.
    issues = hxs.select('//div[@class="issue-cockpit-All"]/div[@class="issue-cockpit-totals"]/a/text()')
    if issues:
      statictics['opened_issues'] = issues.extract()[0].split(' ')[0]
      statictics['total_issues'] = issues.extract()[1].split(' ')[0]

    # Gets the bugs report section.
    bugs = hxs.select('//div[@class="issue-cockpit-bug"]/div[@class="issue-cockpit-totals"]/a/text()')
    if bugs:
      statictics['opened_bugs'] = bugs.extract()[0].split(' ')[0]
      statictics['total_bugs'] = bugs.extract()[1].split(' ')[0]

    # Gets the number of module downloads and installation.
    for stats in hxs.select('//div[contains(@class,"project-info")]/ul/li'):
      if stats.select('text()').extract()[0].startswith('Downloads') :
        statictics['downloads'] = stats.select('text()').extract()[0].split(' ')[1]

      if stats.select('text()').extract()[0].startswith('Reported installs'):
        statictics['installs'] = stats.select('strong/text()').extract()[0]

    yield statictics

