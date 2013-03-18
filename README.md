
<h2> Intro </h2>
	This crawler is built in Python and based on the A-MA-ZING scrapy framework.

	The purpose of this crawler is to scan all the modules hosted on Drupal.org to store them in a database.

<h2> Pre-requisites: </h2>
  In order to make this crawler works, you need to install on your machine :
  <ul>
		<li>Python</li>
		<li>scrapy</li>
	</ul>

<h3>Install scrapy</h3>

The easiest way to install scrapy is to use <strong><a href="https://pypi.python.org/pypi/pip">pip</a></strong> a tool for installing and managing Python packages.

Installing scrapy using pip:

<code>pip install Scrapy</code>

<h3>Download the crawler</h3>

<code>git clone git://github.com/JulienD/modules-crawler.git</code>

<h2> Play with the crawler </h2>

To run the spider :
<code>
	scrapy crawl ModulesXml
</code>

If you want to specify a major version of modules, you can pass it as an argument :
<code>
	scrapy crawl ModulesXml -a version=7
</code>

By default Scrapy display all messages even Debug info, if you want to just see Error message use the loglevel argument :
<code>
	scrapy crawl ModulesXml --loglevel=ERROR
</code>