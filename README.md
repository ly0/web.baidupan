web.baidupan
============

这是一个连接 `aria2-RPC` 的版本

第一次使用请先修改 launcher.py 里 `pcs = PCS('username', 'password')` 成你自己的用户名和密码

并且修改`ARIA2RPC`为服务器能访问到的`RPC`地址（暂时这样，正常情况应该由前端提交而不是后台）

运行:<br>
`python launcher.py`

依赖: <br>
[baidupcsapi](http://github.com/ly0/baidupcsapi) (其他依赖在这个库里了)<br>
[web.py](http://webpy.org)
