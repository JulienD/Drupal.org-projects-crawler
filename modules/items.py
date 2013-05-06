# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class Information(Item):
    project_name = Field()
    project_title = Field()
    #project_description = Field()
    project_type = Field()
    project_url = Field()
    project_git_url = Field()
    pass

class Statistic(Item):
    project_name = Field()
    downloads = Field()
    installs = Field()
    opened_issues = Field()
    total_issues = Field()
    opened_bugs = Field()
    total_bugs = Field()
    pass

class Releases(Item):
    project_name = Field()
    releases = Field()
    pass

class Release(Item):
    release_name = Field()
    release_version = Field()
    release_tag = Field()
    release_date = Field()
    version_major = Field()
    version_patch = Field()
    version_extra = Field()
    pass
