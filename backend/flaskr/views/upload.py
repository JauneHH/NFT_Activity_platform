from flask import request
import requests
from flaskr import app, files, db
from flaskr.Models.middle import PicA, PicU
from flaskr.Models.models import User
from flaskr.views.watermark import addWaterMark


@app.route('/demo/upload', methods=['POST'])
def upload_a_file():
    """
    测试文件发送给区块链平台
    上传一个文件  测试  视图函数view
    :return: url
    """
    if request.method == 'POST' and 'file' in request.files:
        file = request.files['file']
        # save 三个参数分别为 文件 ， 位置 ， 命名
        # 一个文件似乎只能save一次 ？？？
        # filename = files.save(file, 'video', '11111.jpg')
        filename = files.save(file,'platform')
        file_url = files.url(filename)
        print(filename)
        print("upload_a_file")
        return file_url


# 上传文件调用的函数
def upload_files_test(file, location):
    """
    :param file: 文件
    :param location: 文件夹位置
    :return: url
    """
    filename = files.save(file, location)
    file_url = files.url(filename)
    return file_url


def user_upload_save_database(file, userid, activityid):
    """
    用户上传图片 以用户id为文件夹
    并将 url 存入数据库
    且发送文件给平台
    :param file: 文件
    :param userid: 用户id
    :param activityid:  活动id
    :return: url
    """
    location = 'user/' + str(userid)
    print("location = ", location)
    filename = files.save(file, location)
    print("filename = ", filename)
    url = files.url(filename)
    print(url)
    img_id=url.split('.')[-1]

    print(img_id)
    watermark_url = "/root/myflask/flaskr/static/" + filename
    #watermark_url="/Users/huangzexi/PycharmProjects/end_demo11.28/flaskr/static/"+filename

    # 发送 request 给区块链平台
    req_url = "http://127.0.0.1:5000/demo/upload"
    data = None
    # 使用相对路径需要从app.py开始执行，而不是当前upload.py
    # with 关闭 文件指针
    with open("flaskr/static/" + filename, "rb") as fp:
        try:
            req_files = {
                "file": (fp),
            }
            r = requests.post(req_url, data, files=req_files)
        except:
            print('File upload error!')

    if (img_id != "bmp" and img_id != "png" and img_id != "gif" and img_id != "jpg" and img_id != "jpeg"):
        pic = PicU(user=userid, url=url, activity=activityid, type='video')
    else:
        user=User.query.filter(User.user_id==userid).first()
        watermark_name=user.name
        addWaterMark(watermark_url,watermark_name)
        pic = PicU(user=userid, url=url, activity=activityid, type='image')

    db.session.add(pic)
    db.session.commit()
    return url


def activity_upload_save_database(file, activityid):
    """
    活动图片上传 以活动id为文件夹 并将 url 存入数据库
    :param activityid:
    :param file:

    :return:
    """
    location = 'activity/' + str(activityid)
    print(location)
    filename = files.save(file, location)
    print(filename)
    url = files.url(filename)
    print(url)
    pic = PicA(activity=activityid, url=url)
    db.session.add(pic)
    db.session.commit()
    return url
