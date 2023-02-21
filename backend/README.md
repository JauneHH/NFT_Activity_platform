pip install 
flask
sqlalchemy
pymysql
flask-uploads
pip install flask-cors

pip install numpy matplotlib pillow wordcloud imageio jieba snownlp itchat -i https://pypi.tuna.tsinghua.edu.cn/simple


pip install -U Werkzeug==0.16.0 使用此版本有可能报错 cannot import name 'ContextVar' from 'werkzeug.local' 解决方法为使用最新的Werkzeug
https://blog.csdn.net/weixin_43729284/article/details/104771314
https://github.com/maxcountryman/flask-uploads/issues/43
源代码修改为

http://1.116.113.201:8001/

```
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
```

FileStorage在werkzeug.datastructures 下面

```
pip install git+ssh://git@github.com/maxcountryman/flask-uploads
```

or

```
pip install git+https://github.com/maxcountryman/flask-uploads
```

数据库查询，之前  and   或者 使用  and_  都可以使用，但是现在不可以直接使用and
不知道为啥
可能和版本有关。。。。
https://www.cnblogs.com/xiaxiaoxu/p/10597448.html

upload.py里面：
user_upload_save_database(file, userid, activityid, type):
用户上传图片 以用户id为文件夹
并将 url 存入数据库
且发送文件给平台

# 删除 fuser报告进程使用的文件和网络套接字，-k kill
后端启动
1.切换到 myflask 环境
conda activate myflask
2.切换到 文件目录
cd  /root/myflask
3.如要关闭uwsgi和nginx
sudo fuser -k 443/tcp
pkill -f uwsgi -9
4.启动 nginx和uwsgi
uwsgi -d --ini myflask.ini
/usr/sbin/nginx -c /etc/nginx/nginx.conf
修改nginx配置需要去 以上位置替换