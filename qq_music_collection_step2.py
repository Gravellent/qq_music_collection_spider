from pymongo import MongoClient
from urllib.parse import quote_plus
import urllib
import json
import time
from request import req
from db import db, COLLECTION_NAME
import traceback 

COLLECTION_DETAIL_URL = 'https://c.y.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg'
i = 0

# print(db[COLLECTION_NAME].find_one({'status_code': 1}))

for c in db[COLLECTION_NAME].find({'status_code': 1}):
    disstid = c['dissid']

    params = {
        'json': 1,
        'type': 1,
        'utf8': 1,
        'onlysong': 0,
        'disstid': disstid,
        'inCharset': 'utf8',
        'outCharset': 'utf-8',
        'format': 'jsonp',
    }
    try:
        url = '{}?{}'.format(COLLECTION_DETAIL_URL, urllib.parse.urlencode(params))
        res = req(url)
        raw_data = json.loads(res.text[len('jsonCallback('):-1])['cdlist']
    except KeyboardInterrupt:
        break
    except:
        traceback.print_exc()
        continue
    db.qq_music.update_one({'_id': c['_id']}, {
        '$set':{
            'detail': raw_data,
            'status_code': 2,
        }
    })
    i = i+1
    print('Finish processing {}'.format(disstid))
    time.sleep(0.2)