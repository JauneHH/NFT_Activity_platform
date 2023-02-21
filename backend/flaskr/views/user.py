"""
user
用户相关
"""
import json

import requests
import datetime
from flask import request
from flask import render_template
from flaskr import app, db
from flaskr.Models.models import User, Activity,Ticket,User_activity_message
from flaskr.Models.middle import PicU, user_activity_class
from flaskr.views.upload import user_upload_save_database

#
# @app.route('/api/popular_activity', methods=['GET'])
# def hot_activity_information_get():
#     """
#     test 获取滚动栏热门活动信息
#     返回id == 1 的 活动
#     :return: data
#     """
#     a = Activity.query.get(1)
#     print(a)
#     data = {
#         # "msg": "Successfully",
#         'id': a.activity_id,
#         'name': a.activity_name,
#         'area': a.activity_area,
#         'img_url': a.img_url
#     }
#
#     return data

@app.route("/register",methods=['GET','POST'])
def user_register():
    """
    一
    1. 用户登陆权限接口
    对用户登陆小程序进行授权并返回openid唯一用户标示，并且上传用户数据到数据库

    微信发来 code 认证
    用户权限登录
    并将name ， alias ， openid 存入数据库
    :return:
    """
    dict = json.loads(request.get_data().decode('utf-8'))  # 将前端Json数据转为字典
    print(dict)
    encryptedData = dict['platUserInfoMap']['encryptedData']
    code = dict['platCode']  # 前端POST过来的微信临时登录凭证code
    iv = dict['platUserInfoMap']['iv']
    name=dict['userInfo']['nickName']
    gender=dict['userInfo']['gender']
    city = dict['userInfo']['city']
    img_url=dict['userInfo']['avatarUrl']
    alias=dict['userInfo']['nickName']
    req_params = {
        'appid': 'wxa6d0620fbf21f331',  # 开发者关于微信小程序的appID
        'secret': '2614eded10e7a6251dde63963aacc28e',  # 开发者关于微信小程序的appSecret
        'js_code': code,
        'grant_type': 'authorization_code'
    }
    req_result = requests.get('https://api.weixin.qq.com/sns/jscode2session',
                              params=req_params, timeout=3,verify=False)
    print(req_result,'req_result')
    resData = req_result.json()
    print(resData)
    open_id = resData['openid']  # 得到用户关于当前小程序的OpenID
    session_key = resData['session_key']  # 得到用户关于当前小程序的会话密钥session_key
    #获取openid进行查询
    #user_test= User.query.filter_by(open_id = 'xiaoyi').all()
    user = User.query.filter_by(open_id=open_id).first()
    print(user)

    #用户是否第一次注册
    if ((User.query.filter_by(open_id = open_id).first())):
        user = User.query.filter_by(open_id=open_id).first()
        print(user)
        print('exist')
        resData['userid']=user.user_id
        resData['photographer'] = user.photographer
        return resData
    else:
        print('notexist')
        u = User(
            name=name,
            open_id=open_id,
            male = gender,
            city = city,
            img_url =img_url,
            alias=alias
        )
        db.session.add(u)
        db.session.commit()
        UserItem=User.query.filter_by(open_id=open_id).first()
        resData['userid'] = UserItem.user_id
        resData['photographer']=UserItem.photographer
        return resData



@app.route('/api/general_information', methods=['POST'])
def user_information_get():
    """
    一
    2 个人信息
    获取用户个人的所有信息
    :return:
    """
    r = request.get_data()
    print(r)
    print(type(r))
    dict1 = json.loads(r)  # 重新编码
    print(dict1)

    # open_id = request.form['open_id'] 使用表单form的情况，此时使用的为json
    #open_id = dict1['open_id']
    uid = dict1['user_id']
    #print(open_id)
    # signature = dict['signature']
    # print(signature)
    user = User.query.filter(User.user_id == uid).first_or_404()
    print(user)
    data = {
        'id': user.user_id,
        'name': user.name,
        'alias': user.alias,
        'img_url': user.img_url,
        'open_id': user.open_id,
        'photographer':user.photographer,
        'point': user.point
        # 'activities_num': user.activities_num,
        # 'coupons_num': user.coupons_num
    }
    print(data)
    return data



@app.route('/api/activity_attend', methods=['POST'])
def user_attend_activity():
    """
    一
    3 用户参加活动
    :return:
    """
    r = request.get_data()
    print(r)
    dict = json.loads(r)  # 重新编码
    print(dict)

    activity_id = dict['activity_id']
    print(activity_id)
    user_id = dict['user_id']
    print(user_id)

    a = Activity.query.get(activity_id)
    u = User.query.get(user_id)
    a.users.append(u)

    u_a_class = user_activity_class(
        user_id=user_id,
        user_name=u.name,
        activity_id=activity_id,
        attend_date=datetime.datetime.now(),
        activity_name=a.activity_name,
        city = u.city,
        male = u.male
    )
    db.session.add(u_a_class)

    db.session.commit()
    return "用户已经参加活动"


@app.route('/api/activity_finished', methods=['POST'])
def user_activity_finished():
    """
    一
    4 用户完成活动   使用 form  上传文件
    用户上传视频、图片完成活动
    :return:
    """
    uid = request.form['user_id']
    print("uid = ", uid)
    aid = request.form['activity_id']
    print("aid = ", aid)

    file = request.files['file']
    url = user_upload_save_database(file, uid, aid)
    print("url = ", url)
    return str(url)


    """
    返回上传的图片和视频  数组
    :return:
    不用
    """
@app.route('/api/activity_finished_img', methods=['GET'])
def user_activity_finished_img():
    """
    5.返回用户上传的图片和视频  数组
    :return:
    """
    r = request.get_data()
    dict = json.loads(r)  # 重新编码
    uid = dict['user_id']
    print("uid = ", uid)
    aid = dict['activity_id']
    print("aid = ", aid)
    u_a=user_activity_class.query.filter(
        user_activity_class.user_id == uid, user_activity_class.activity_id == aid
    ).first()
    pics = PicU.query.filter(
        PicU.user == uid, PicU.activity == aid
    ).all()
    print(pics)
    pic_list = []
    for pic in pics:
        url = pic.url
        print(url)
        pic_list.append(url)

    data = {
        "img_list":pic_list,
        'feedback_message':u_a.feedback_message
    }
    print(data)
    return data




@app.route('/api/user/activity_user_imgs', methods=['POST'])
def user_watch_upload_imgs():
    """
    6. 用户查看活动情况
    查看自己已经上传的图片信息,评论
    :return:
    """
    r = request.get_data()
    print(r)
    dict = json.loads(r)  # 重新编码
    print(dict)

    uid = dict['user_id']
    print(uid)
    aid = dict['activity_id']
    print(aid)

    pics = PicU.query.filter(
        PicU.user == uid ,
        PicU.activity == aid
    ).all()

    data = {}
    pic_list = []
    for pic in pics:
        url = pic.url
        print(url)
        pic_list.append(url)
    print(pic_list)
    data = {
        "img_list": pic_list
    }

    uac = user_activity_class.query.filter(
        user_activity_class.user_id == uid,
        user_activity_class.activity_id == aid
    ).first()
    print(uac.feedback_message)

    data["comment"] = uac.comment
    data["user_activity_status"] = uac.user_activity_status
    data["feedback_message"]= uac.feedback_message
    data["production_rate"] = uac.production_rate
    data["booth_rate"] = uac.booth_rate
    data["service_rate"] = uac.service_rate
    data["activity_rate"] = uac.activity_rate

    print(data)
    return data


@app.route('/api/activity_finished_comment', methods=['POST'])
def user_activity_finished_comment():
    """
    7.用户添加活动的评论
    :return:
    """
    r = request.get_data()
    print(r)
    dict = json.loads(r)  # 重新编码
    print(dict)

    uid = dict['user_id']
    print("uid = ", uid)
    aid = dict['activity_id']
    print("aid = ", aid)
    comment = dict['comment']
    production_rate = dict['production_rate']
    booth_rate = dict['booth_rate']
    service_rate = dict['service_rate']
    activity_rate = dict['activity_rate']
    print(comment)
    uac = user_activity_class.query.filter(
        user_activity_class.user_id == uid, user_activity_class.activity_id == aid
    ).first()
    picu = PicU.query.filter(PicU.user == uid, PicU.activity == aid).all()
    for item in picu:
        db.session.delete(item)

    uac.comment = comment
    uac.production_rate=production_rate
    uac.booth_rate = booth_rate
    uac.service_rate = service_rate
    uac.activity_rate = activity_rate
    uac.user_activity_status = 1
    db.session.commit()
    return "已经完成评论"





@app.route('/api/activity_prize', methods=['POST'])
def user_activity_prize():
    """
    一
    8. 用户获取活动奖励
    活动方审核完成后，用户获取完成活动获得奖励，例如电影票兑换
    :return:
    """
    uid = dict['user_id']
    print(uid)

    return "coupon id=dnbashjbnisa"




@app.route('/api/User_photographer', methods=['POST'])
def User_photographer():
    """
    9 用户选择是否为摄影师
    :return:
    """
    r = request.get_data()
    print(r)
    dict = json.loads(r)  # 重新编码
    print(dict)

    uid = dict['user_id']
    user=User.query.filter(User.user_id==uid).first()

    return {'photographer':user.photographer}

@app.route('/api/notice', methods=['POST'])
def notice():
    """
    10 新消息提醒
    :return:
    """
    r = request.get_data()
    print(r)
    dict = json.loads(r)  # 重新编码
    print(dict)

    uid = dict['user_id']
    #user_message=user_activity_class.query.filter(user_activity_class.user_id==uid).all()

    message=User_activity_message.query.filter(User_activity_message.user_id==uid).order_by(User_activity_message.time.desc()).all()

    Data = []
    for item in message:

        activity_item = Activity.query.filter(Activity.activity_id == item.activity_id).first()
        user_activity=user_activity_class.query.filter(user_activity_class.activity_id==item.activity_id,user_activity_class.user_id==uid).first()
        data = {}
        data['activity_id']=activity_item.activity_id
        data['message']=item.feedback_message
        data['activity_name']=activity_item.activity_name
        data['user_activity_status']=item.user_activity_status
        data['has_read']=item.has_read
        data['img_url'] = activity_item.img_url
        data['ticket_name'] = item.ticket_name
        data['NFT_name'] = item.NFT_name
        data['NFT_url'] = item.NFT_url
        ticket=Ticket.query.filter(Ticket.user_id==uid,Ticket.activity_id==activity_item.activity_id).all()
        i=0
        for item in ticket:
            i=i+1
        if(i!=0):
            data['ticket']=i
        Data.append(data)
        print(Data)

    return {'msg':Data}

@app.route('/api/change_notice', methods=['POST'])
def change_notice():
    """
    11 修改为已读
    :return:
    """
    r = request.get_data()
    print(r)
    dict = json.loads(r)  # 重新编码
    print(dict)

    uid = dict['user_id']
    user_message=user_activity_class.query.filter(user_activity_class.user_id==uid).all()

    Data = []
    message = User_activity_message.query.filter(User_activity_message.user_id == uid).order_by(User_activity_message.time.desc()).all()
    print(message)
    for item in message:
        if (item.has_read == 0):
            item.has_read = 1
    db.session.commit()
    return {'msg':Data}


@app.route('/api/user_ticket', methods=['POST'])
def user_ticket():
    """
    12 用户ticket
    :return:
    """
    r = request.get_data()
    print(r)
    dict = json.loads(r)  # 重新编码
    print(dict)

    uid = dict['user_id']
    ticket=Ticket.query.filter(Ticket.user_id==uid).all()
    print(ticket)
    Data = []
    for item in ticket:
        item.has_receive=1

        data = {}
        data['ticket_name'] = item.name
        data['exchange_code'] = item.exchange_code
        data['password'] = item.password
        data['has_receive'] = item.has_receive
        data['get_time'] = item.get_time.strftime("%Y-%m-%d %H:%M:%S")
        Data.append(data)
    db.session.commit()
    return {'msg':Data}

@app.route('/api/index_ticket', methods=['POST'])
def index_ticket():
    """
    13 首页ticket
    :return:
    """
    r = request.get_data()
    print(r)
    dict = json.loads(r)  # 重新编码
    print(dict)

    uid = dict['user_id']
    ticket=Ticket.query.filter(Ticket.user_id==uid).all()
    print(ticket)
    Data = []
    for item in ticket:

        data = {}
        data['ticket_name'] = item.name
        data['exchange_code'] = item.exchange_code
        data['password'] = item.password
        data['has_receive'] = item.has_receive
        data['get_time'] = item.get_time.strftime("%Y-%m-%d %H:%M:%S")
        Data.append(data)

    return {'msg':Data}