from pymongo import MongoClient
from urllib.parse import quote_plus
import urllib
import json
import time

COLLECTION_DETAIL_URL = 'https://c.y.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg'
# MONGO_HOST = '10.23.74.21'
# MONGO_USER = 'martin'
# MONGO_PASS = '12345678'
# uri = "mongodb://%s:%s@%s" % (
#     quote_plus(MONGO_USER), quote_plus(MONGO_PASS), MONGO_HOST)
# client = MongoClient(uri)
client = MongoClient('127.0.0.1', 27017)
db = client.music
# print(db.m.find_one())

i = 0


import requests

def req(targetUrl, headers = {}):
    # 要访问的目标页面
    # targetUrl = "http://test.abuyun.com"

    # 代理服务器
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"

    # 代理隧道验证信息
    proxyUser = "HIB99U62Q6Z03W8D"
    proxyPass = "343B105171BF1FA1"

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
      "host" : proxyHost,
      "port" : proxyPort,
      "user" : proxyUser,
      "pass" : proxyPass,
    }

    proxies = {
        "http"  : proxyMeta,
        "https" : proxyMeta,
    }

    resp = requests.get(targetUrl, proxies=proxies, headers=headers)
    
    return resp

# print (resp.status_code)
# print (resp.text)           

for c in db.qq_music.find({'status_code': 1}):
    if c['status_code'] > 1:
        pass
    else:

        disstid = c['dissid']
        headers= {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
            'Referer': 'https://y.qq.com/portal/playlist.html',
        }

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
            res = req(url, headers=headers)
            raw_data = json.loads(res.text[len('jsonCallback('):-1])['cdlist']
        except KeyboardInterrupt:
            break
        except:
            continue
        db.qq_music.update_one({'_id': c['_id']}, {
            '$set':{
                'detail': raw_data,
                'status_code': 2,
            }
        i = i+1
        print(i)
        time.sleep(0.2)