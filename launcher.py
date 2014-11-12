# coding=utf-8
import json
import os
import web
import re
import sys
import urllib2
import modules.aria2rpc as aria2rpc
from baidupcsapi import *

# config aria2 rpc address, json rpc needed.
ARIA2RPC = 'http://127.0.0.1:6800/jsonrpc'

# user-defined prefix of baidupcs CDN node
# comment next line if you want to keep origin url that server returns
# PRIOR_NODE = 'nb'

# Baidupcs account setting
ACCOUNT = {
    'username': '',
    'password': ''
}


urls = (
    '/', 'Index',
    '/static/(.*)', 'Resource',
    '/download/(.*)', 'Download',
    '/file/(.*)', 'File',
    '/lx', 'Lixian',
    '/lx/(\d+)', 'LixianDownload',
    '/list(.*)', 'List',
    '/info/([^/]+)', 'Info'
)

aria = aria2rpc.Aria2RPC(ARIA2RPC)

# source: baidupcsapi repo Issue 3 on github


def upload_img42(img):
    url = 'http://img42.com'
    req = urllib2.Request(url, data=img)
    msg = urllib2.urlopen(req).read()
    return '%s/%s' % (url, json.loads(msg)['id'])


def captcha(jpeg):
    print '[*]', 'captcha needed'
    print 'captcha url:', upload_img42(jpeg)
    foo = raw_input('captcha >')
    return foo


class Index:

    def GET(self, *args):
        # return pcs.list_files('/').content
        render = web.template.render('templates')
        data = {
            'modules': {'web.ctx': web.ctx, }
        }
        return render.list_files(data=data)


class File:

    def GET(self, *args):
        # return pcs.list_files('/').content
        render = web.template.render('templates')
        data = {
            'modules': {'web.ctx': web.ctx, }
        }
        return render.list_files(data=data)


class List:

    def GET(self, *args):
        if len(args) != 1:
            return web.notfound('parameter error')

        data = json.loads(pcs.list_files('/'.join(args)).content)['list']
        return json.dumps(data)


class Info:

    def GET(self, *args):
        if len(args) != 1:
            return web.notfound('parameter error')
        arg = args[0]

        if arg == 'quota':
            return pcs.quota().content


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

        if 'PRIOR_NODE' in globals() and 'cdn.baidupcs.com' not in download_url:
            url = re.sub('http://(.*?)\.baidupcs\.com',
                         'http://' + PRIOR_NODE + '.baidupcs.com',
                         download_url)
        else:
            url = download_url

        # add aria2 task
        ret = aria.add_uris(url,
                            header=['User-Agent: WindowsBaiduYunGuanJia'])
        return "Aria2 ID:" + ret

class LixianDownload:

    def GET(self, *args):
        try:
            download_id = args[0]
        except:
            return web.notfound('parameter error')
        jdata = pcs.query_download_tasks([download_id]).content
        if 'error_code' in json.loads(jdata):
            return web.notfound('404 Lixian task not found')
        return pcs.query_download_tasks([download_id]).content


class Lixian:

    def GET(self, *args):
        path = '/' + '/'.join(args)
        return json.dumps(json.loads(pcs.list_download_tasks(limit=5).content)['task_info'])

    def POST(self, *args):
        return 'POST'


def print_config():
    print '[+]', 'BaiduPCS account setting'
    print ACCOUNT
    print '[+]', 'Aria2 RPC address:', ARIA2RPC


def aria_local():
    if ARIA2RPC.startswith('http://localhost') \
            or ARIA2RPC.startswith('http://127.0.0.1'):
        # start aria2c
        print '[+]', 'Your aria2 rpc is on localhost'
        if os.system('pidof aria2c') == 0:
            print '[+]', 'Aria2c is running.'
        else:
            print '[*]', 'Booting aria2c'
            ret = os.system('aria2c -D --enable-rpc')
            if ret != 0:
                print '[x]', 'Aria2c can not run, retcode=', ret
                sys.exit(256)

if __name__ == "__main__":
    web.config.debug = False  # turn off debug mode
    # print config
    print_config()
    print 'Connecting to baidu ...'
    pcs = PCS(
        ACCOUNT['username'], ACCOUNT['password'], captcha_callback=captcha)
    print 'Connected'
    app = web.application(urls, globals())
    app.run()
