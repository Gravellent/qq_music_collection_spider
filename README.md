# qq_music_collection_crawler


## Purpose

Crawl collection information from QQ music for further data analysis. The crawlers will first try to retrive data from QQ music collection homepage, then it goes to detail page to get the list of songs. The two crawlers are separated into two files. The first file "qq_music_collection_step1.py" will crawl the basic information of the collection and store to the Mongo Database. The second file "qq_music_collection_step2.py" gets the detail informaiton form the detial page.

## Python version

Python 3.6.5

## How to run

1. Install virtualenv 

`pip install virtualenv`

2. activate virutalenv & source

`cd [project_path]`  
`virtualenv .venv`  
`source .venv/bin/activate/ --python=python3`  

3. Install packages
`pip install -r requirements.txt`

4. Set up MongoDB connection
Depending on your Mongo set up, you need to configure the uri in settings.py in order to store to the database. Modify settings.py.example to proceed.

5. Modify request.py
Likely you would need some kind of IP rotation to avoid being banned. Modify the request.py file and add proxy in it.

6. Run first script
`python qq_music_collection_step1.py`
This will get the basic information of the collections from homepage

7. Run second script
`python qq_music_collection_step2.py`
This will get the detail information of each collection, obtained from the first step

## Avoid getting banned

Known anti-crawling mechanism
1. Need set referer in header for each request
2. Need set User-Agent
3. IP rotation (hasn't tested yet)