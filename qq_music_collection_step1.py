# coding: utf-8

# # QQ Music Crawlers
import json
import csv
import urllib
import datetime
import time
from pprint import pprint
from bson import ObjectId
import traceback

from request import req
from db import db, insert, COLLECTION_NAME
### Convert output

def adapt_output(diss):
    d = diss.copy()
    d['createtime'] = datetime.datetime.strptime(diss['createtime'], '%Y-%m-%d')
    d['commit_time'] = datetime.datetime.strptime(diss['createtime'], '%Y-%m-%d')
    d['download_time'] = datetime.datetime.now()
    d['status_code'] = 1 
    return d

""" Read the categories into a list"""
cids = []
with open('categories.txt', 'r') as f:
    reader = csv.reader(f)
    for r in reader:
        cids.append(r[0])   


"""Construct Data API URLs"""

COLLECTION_API_URL = 'https://c.y.qq.com/splcloud/fcgi-bin/fcg_get_diss_by_tag.fcg'
PAGE_SIZE = 29

print("Start crawling")

for cid in cids:

    exit = False
    sortId = 5
    start = 0
    retry = 0

    print("Getting category_id = {}".format(cid))
    while True:
        new_diss = []

        # Construct url params
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
            collections = req(url).json()
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

            # If failed tried three times and failed, pass to the next one
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

