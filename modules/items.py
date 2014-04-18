# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class Project(Item):
    name = Field()
    information = Field()
    statistics = Field()
    releases = Field()
    pass

class Information(Item):
    title = Field()
    description = Field()
    type = Field()
    url = Field()
    git_url = Field()
    api_version = Field()
    recommended_major = Field()
    supported_majors = Field()
    default_major = Field()
    last_commit = Field()
    pass

class Statistic(Item):
    downloads = Field()
    installs = Field()
    opened_issues = Field()
    total_issues = Field()
    opened_bugs = Field()
    total_bugs = Field()
    pass

class Release(Item):
    name = Field()
    version = Field()
    tag = Field()
    date = Field()
    version_major = Field()
    version_patch = Field()
    version_extra = Field()
    pass

class maintainer(Item):
    maintainer_id = Field()
    pass