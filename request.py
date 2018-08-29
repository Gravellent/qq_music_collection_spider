import requests

def req(targetUrl):
    
    """ You can add the proxy settings here"""
    headers= {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
        'Referer': 'https://y.qq.com/portal/playlist.html',
    }
    
    resp = requests.get(targetUrl,  headers=headers)
    return resp