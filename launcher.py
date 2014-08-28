#coding=utf-8
import json
import os
import web
import time
from baidupcsapi import *

# urls support regular expression
# request will be sent with arguments of re's groups

urls = (
    '/', 'Index',
    '/static/(.*)', 'Resource',
    '/download/(.*)', 'Download',
    '/file/(.*)', 'File'
)

pcs = PCS('username', 'password')


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
                            'web.ctx': web.ctx}
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
                            'round': round}
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
        return web.redirect(pcs.download_url(path)[0])

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
