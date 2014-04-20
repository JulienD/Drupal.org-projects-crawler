#!/bin/bash

download=false

# Gets the XML file and gets its creation date.
file_name="/tmp/drupal-project-release-7.xml"
creation_date=$(date -r $file_name +%s)

echo $creation_date

# Checks if the xml file exists.
if [[ -z $creation_date ]]
then
    # Mark the file has need to be downloaded.
    download=true
else
    # Check the validity of the xml file.
    current_time=$(date +%s)

    # Convert diff in minutes.
    (( diff=diff/3600 ))

    if ($diff > 24)
    then
        download=true
    fi
fi

if ($download = true)
then
    curl -o /tmp/drupal-project-release-7.xml http://updates.drupal.org/release-history/project-list/all/7
fi

/usr/bin/scrapy crawl ModulesXml
