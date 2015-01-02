web.baidupan
============

第一次使用请先修改 launcher.py 里 `pcs = PCS('username', 'password')` 成你自己的用户名和密码

最新版请切换到 dev 分支

纯属娱乐, 代码丑陋功能简略, javascript什么的毛也不会, 离线任务懒得弄了, 可以把模板复制粘贴一份调用*baidupcsapi*的接口就好.

TODOLIST
------------
- [ ] 在需要输入验证码的时候由访问者输入
- [ ] 获得离线下载资源
- [ ] 在线提交离线下载
- [ ] 保存指定的百度盘分享链接到本盘
- [ ] 分享指定文件(列表)和文件夹
- [ ] 自动识别百度的验证码
- [X] 加入修改user-agent的提示
- [ ] 支持多百度帐号

已知BUG
------------
- [X] 获得下载地址的接口会因为时间原因失效


截图:
![image](https://raw.githubusercontent.com/ly0/web.baidupan/master/screenshot.png)

运行:<br>
`python launcher.py`

依赖: <br>
[baidupcsapi](http://github.com/ly0/baidupcsapi) (其他依赖在这个库里了)<br>
[web.py](http://webpy.org)
