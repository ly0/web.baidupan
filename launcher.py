#coding=utf-8
import json
import os
import web
import time
import re
import urllib2
import getpass
from baidupcsapi import *

urls = (
    '/', 'Index',
    '/static/(.*)', 'Resource',
    '/download/(.*)', 'Download',
    '/file/(.*)', 'File',
    '/lx', 'Lixian',
    '/lx/(\d+)', 'LixianDownload',
    '/stream/(.*)', 'Stream'
)

# source: baidupcsapi repo Issue 3 on github
def upload_img42(img):
    url = 'http://img42.com'
    req = urllib2.Request(url, data=img)
    msg = urllib2.urlopen(req).read()
    return '%s/%s' % (url, json.loads(msg)['id'])

def captcha(jpeg):
    print '* captcha needed'
    print 'captcha url:', upload_img42(jpeg)
    foo = raw_input('captcha >')
    return foo

# edited

pcs = PCS('', '', captcha_callback=captcha)
# user-defined prefix of baidupcs CDN node
# comment next line if you want to keep origin url that server returns
PRIOR_NODE = 'nb' 

def self_round(n, d):
    return round(n, d)


class Index:
    def GET(self, *args):
        # return pcs.list_files('/').content
        render = web.template.render('templates')
        data = {'pcs': json.loads(pcs.list_files('/').content)['list'],
                'quota': json.loads(pcs.quota().content),
                'pcsobj': pcs,
                'modules': {'time': time,
                            'round': round,
                            'web.ctx': web.ctx,
                            'lib_json': json}
                }
        return render.list_files(data=data)


class File:
    def GET(self, *args):
        # return pcs.list_files('/').content
        render = web.template.render('templates')
        data = {'pcs': json.loads(pcs.list_files('/' + '/'.join(args)).content)['list'],
                'quota': json.loads(pcs.quota().content),
                'pcsobj': pcs,
                'modules': {'time': time,
                            'round': round,
                            'web.ctx': web.ctx,
                            'lib_json': json}
                }
        return render.list_files(data=data)


class Resource:
    def GET(self, *args):
        path = os.path.join('static', '/'.join(args))
        if not os.path.exists(path):
            return web.notfound('Resource not found.')

        with open(path, 'r') as fp:
            content = fp.read()
        return content


class Download:
    def GET(self, *args):
        path = '/' + '/'.join(args)
        # user-defined baidupcs CDN node
        download_url = pcs.download_url(path)[0]
        if 'PRIOR_NODE' in globals() and 'cdn.baidupcs.com' not in download_url :
            return re.sub('http://(.*?)\.baidupcs\.com', 'http://' + PRIOR_NODE + '.baidupcs.com', download_url)
        else:
            return download_url

class LixianDownload:
    def GET(self, *args):
        try:
            download_id = args[0]
        except:
            return web.notfound('Lixian task not found')
        return pcs.query_download_tasks([download_id]).content


class Lixian:
    def GET(self, *args):
        path = '/' + '/'.join(args)
        return json.dumps(json.loads(pcs.list_download_tasks(limit=5).content)['task_info'])

    def POST(self, *args):
        return 'POST'

class Stream:
    def GET(self, *args):
        path = '/' + '/'.join(args)
        if 'type' in web.input():
            stype = web.input()['type']
        else:
            stype = 'M3U8_AUTO_480'
        content = pcs.get_streaming(path=path, stype=stype)
        if isinstance(content, int):
            web.ctx.status = '400 Bad Request'
            if content == 31066:
                return 'file is not existed.'
            elif content == 31304:
                return 'file type is not supported.'
            elif content == 31023:
                return 'param error.'
            else:
                return 'unknown error.'
        return content

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
