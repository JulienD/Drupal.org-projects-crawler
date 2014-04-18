#!/bin/bash

# be sure to change both virtualenv directory and scrape/living_social
# directory to where your venv and code is.
touch /tmp/test/test-scrap.txt
cd /home/vagrant/public_html/python/drupal-projects-crawler
/usr/local/bin/scrapy crawl ModulesXml
