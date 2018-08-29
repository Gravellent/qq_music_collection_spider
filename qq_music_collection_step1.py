# coding: utf-8

# # QQ Music Crawlers
import requests
import json
import csv
from pymongo import MongoClient
import urllib
import datetime
import time
from pprint import pprint
from bson import ObjectId
import traceback


def req(targetUrl, headers = {}):
    resp = requests.get(targetUrl,  headers=headers)
    
    return resp

### Convert output

def adapt_output(diss):
    d = diss.copy()
    d['createtime'] = datetime.datetime.strptime(diss['createtime'], '%Y-%m-%d')
    d['commit_time'] = datetime.datetime.strptime(diss['createtime'], '%Y-%m-%d')
    d['download_time'] = datetime.datetime.now()
    return d


cids = []
with open('categories.txt', 'r') as f:
    reader = csv.reader(f)
    for r in reader:
        cids.append(r[0])   


client = MongoClient('localhost', 27017) # Configure relavent client here
db = client.music

def insert(doc):
    db.qq_music_collection.insert_one(doc)


"""Construct Data API URLs"""

COLLECTION_API_URL = 'https://c.y.qq.com/splcloud/fcgi-bin/fcg_get_diss_by_tag.fcg'
PAGE_SIZE = 29

for cid in cids:
    
    exit = False
    sortId = 5
    start = 0
    retry = 0
    
    while True:
        new_diss = []

        headers= {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
            'Referer': 'https://y.qq.com/portal/playlist.html',
        }

        params = {
            'inCharset': 'utf8',
            'outCharset': 'utf-8',
            'categoryId': cid,
            'sortId': sortId,
            'sin': start,
            'ein': start + PAGE_SIZE,
            'format': 'json',
        }

        url = '{}?{}'.format(COLLECTION_API_URL, urllib.parse.urlencode(params))
        
        try:
            collections = req(url, headers=headers).json()
            if not collections['data']['list']:
                break
            for d in collections['data']['list']:
                insert(adapt_output(d))
            print('Finished process page {}'.format(start))
            retry = 0
        except KeyboardInterrupt:
            exit = True
            break
        except:
            print(url)
            traceback.print_exc()
            
            retry += 1
            if retry > 3:
                break
            else:
                print('Retried')
                pass
        
        start += 30
        time.sleep(0.2)
    
    if exit:
        break

