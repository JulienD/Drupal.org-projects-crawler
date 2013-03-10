# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class Module(Item):
    name = Field()
    title = Field()
    project_url = Field()
    git_url = Field()
    version = Field()
    pass