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
    '/(js)/(.*)', 'Resource',
    '/(css)/(.*)', 'Resource',
    '/download/(.*)', 'Download',
    '/file/(.*)', 'File',
    '/lixian', 'Lixian',
    '/stream/(.*)', 'Stream'
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
        path = os.path.join('./static', '/'.join(args))
        with open(path, 'r') as fp:
            content = fp.read()
        return content


class Download:
    def GET(self, *args):
        path = '/' + '/'.join(args)
        return pcs.download_url(path)[0]


class Lixian:
    def GET(self):
        start = 0
        ret = []
        while True:
            foo = json.loads(pcs.list_download_tasks(start=start,limit=100).content)['task_info']
            if foo:
                ret.extend(foo)
                start = start + 100
                continue
            break
        return str(ret)


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
   


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
