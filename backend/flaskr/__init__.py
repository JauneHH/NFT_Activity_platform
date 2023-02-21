"""
flaskr  __init__
配置文件
"""
import os
import pymysql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # 导入扩展类
from flask_uploads import UploadSet, configure_uploads, ALL
from flask_cors import *

pymysql.install_as_MySQLdb()

app = Flask(__name__, template_folder='templates',static_folder='static-vue',static_url_path='/static-vue')
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:13879275612a@127.0.0.1/ip_test"
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:574343gcf@1.116.113.201/end_demo1"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:13879275612a@127.0.0.1/ip_test"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
# app.config['SECRET_KEY'] = 'dev'  # 等同于 app.secret_key = 'dev'
app.config['UPLOADED_FILES_DEST'] = os.getcwd() + '/flaskr/static'

files = UploadSet('files', ALL)

configure_uploads(app, files)
db = SQLAlchemy(app)

CORS(app, supports_credentials=True)
