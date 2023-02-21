import json

from flask import request
import datetime

from flaskr import app, db
from flaskr.Models.models import User, Activity,Market,Ticket,User_activity_message
from flaskr.Models.middle import user_activity_class, PicU, PicA
from flaskr.views.upload import activity_upload_save_database

"""
########## 活动 ##############
"""


@app.route('/api/activity0', methods=['POST'])
def activity_information_get0():
    """
    test. 获取 地点 类型 符合条件的活动信息   gcf
    :return:
    """
    r = request.get_data()
    print(r)  # 此时  r为  b'{"area": "\\u4e0a\\u6d77", "celebrity": "\\u7535\\u5f71"}'
    dic1 = json.loads(r)  # 重新编码
    print(dic1)  # {'area': '上海', 'celebrity': '电影'}

    area = dic1['area']
    print(area)
    ty = dic1['type']
    print(ty)
    # and
    # filter(条件1 , 条件2)
    activities = Activity.query.filter(
        Activity.activity_area == area, Activity.activity_type == ty).all()
    print(activities)
    print(type(activities))

    Data = {}
    i = 0
    for activity in activities:
        data = {}
        print(activity, "    ",
              activity.activity_name, "         ",
              activity.activity_id, "    ",
              activity.img_url, "    ",
              activity.activity_type)

        data['id'] = activity.activity_id
        data['name'] = activity.activity_name
        # data['area'] = activity.activity_area
        data['img_url'] = activity.img_url
        Data[str(i)] = data
        i = i + 1
        # print(type(activity))

    return Data, 201


@app.route('/api/activity_list', methods=['GET', 'POST'])
def activity_information_get():
    """
    2.1 活动列表
    1. 获取所有活动信息
    :return:
    """
    activities = Activity.query.order_by(Activity.activity_time.desc()).all()
    print(activities)
    # print(type(activitys))

    Data = {}
    activity_type_sum = []  # 活动总共有多少类型
    i = 0
    Datetime=datetime.datetime.now()
    print(Datetime)

    for activity in activities:
        data = {}
        activity_status=activity.activity_status
        print(Datetime-activity.activity_time,Datetime>activity.activity_time)
        if(activity.activity_status==0):
            if(Datetime>activity.activity_time and Datetime<activity.activity_end_time):
                activity.activity_status=1
                activity_status=1
        if ( Datetime > activity.activity_end_time):
            activity.activity_status = 2
            activity_status = 2

        print(activity, "    ",
              activity.activity_name, "         ",
              activity.activity_id, "    ",
              activity.img_url, "    ",
              activity.activity_type, "    ",
              activity.activity_area, "    ",
              activity.activity_time, "    ",
              )
        otherStyleTime = activity.activity_time.strftime("%Y-%m-%d %H:%M:%S")
        print(otherStyleTime)
        # 数据库 2021-08-27 13:36:50

        data['id'] = activity.activity_id
        data['name'] = activity.activity_name
        data['area'] = activity.activity_area
        data['img_url'] = activity.img_url
        data['type'] = activity.activity_type
        data['time'] = activity.activity_time.strftime("%Y-%m-%d %H:%M:%S")
        data['end_time'] = activity.activity_end_time.strftime("%Y-%m-%d %H:%M:%S")
        data['activity_status'] = activity_status
        if activity.activity_type not in activity_type_sum:
            activity_type_sum.append(activity.activity_type)
        Data[str(i)] = data
        i = i + 1
    print(activity_type_sum)
    db.session.commit()
    activity_type_sum_str = str(activity_type_sum)
    Data['type_sum'] = activity_type_sum_str

    return Data


@app.route('/api/activity_search', methods=['POST'])
def activity_information_search():
    """
    2.2 查询活动
    活动 模糊查询  使用活动名称 name
    :return:
    """
    r = request.get_data()
    print(r)
    dict = json.loads(r)  # 重新编码
    print(dict)
    name = dict['name']
    print(name)

    activities = Activity.query.filter(
        Activity.activity_name.like("%" + name + "%")).all()
    num = len(activities)
    print(activities)
    print(num)

    Data = {
        "activities_num": num,
    }
    i = 0
    for activity in activities:
        data = {}

        data['id'] = activity.activity_id
        data['img_url'] = activity.img_url
        data['name'] = activity.activity_name
        data['description'] = activity.activity_description
        data['area'] = activity.activity_area
        data['time'] = activity.activity_time.strftime("%Y-%m-%d %H:%M:%S")
        data['end_time'] = activity.activity_end_time.strftime("%Y-%m-%d %H:%M:%S")
        data['type'] = activity.activity_type
        data['users_number'] = activity.activity_users_number
        data['activity_status'] = activity.activity_status
        Data[str(i)] = data
        i = i + 1

    return Data


@app.route('/api/activity_user', methods=['POST'])
def user_activity_information_get():
    """
    2.3 个人参与的活动信息
    获取用户所参与的各个活动信息
    :return:
    """
    r = request.get_data()
    print(r)
    dict = json.loads(r)  # 重新编码
    print(dict)

    open_id = dict['open_id']
    print(open_id)

    # signature = dict['signature']
    # print(signature)

    user = User.query.filter(User.open_id == open_id).first_or_404()

    user_activity=user_activity_class.query.filter(user_activity_class.user_id==user.user_id).order_by(user_activity_class.attend_date.desc()).all()


    Data = {

    }
    i = 0
    user_id = user.user_id  # 查询是否已经参与
    for item in user_activity:
        activity = Activity.query.filter(Activity.activity_id == item.activity_id).first()
        data = {}
        a_id = activity.activity_id
        print("+++++++++++++++++++++++++++++++++++")
        print("user_id      ", user_id)
        print("a_id    ", a_id)
        u_a_query = user_activity_class.query.filter(
            user_activity_class.user_id == user_id,
            user_activity_class.activity_id == a_id
        ).first()

        print("u_a_query       ", u_a_query)
        print("u_a_query       ", type(u_a_query))

        status = u_a_query.user_activity_status
        print("status = ", status)

        data['id'] = activity.activity_id
        data['name'] = activity.activity_name
        data['area'] = activity.activity_area
        data['img_url'] = activity.img_url
        data['time'] = activity.activity_time.strftime("%Y-%m-%d %H:%M:%S")
        data['end_time'] = activity.activity_end_time.strftime("%Y-%m-%d %H:%M:%S")
        data['type'] = activity.activity_type
        data['status'] = status

        Data[str(i)] = data
        i = i + 1
        print(Data)
    return Data


@app.route('/api/activity_information', methods=['POST'])
def activity_information_get_by_id():
    """
    2.4 具体活动信息
    获取每个活动的具体信息数据返回给前端 根据 id
    :return:
    """
    print('activity_information')
    r = request.get_data()
    dict = json.loads(r)  # 重新编码
    print(dict)
    aid = dict['id']

    has_attend = 0

    activity = Activity.query.get(aid)
    print(activity)
    data = {}
    data['id'] = activity.activity_id
    data['img_url'] = activity.img_url
    data['name'] = activity.activity_name
    data['area'] = activity.activity_area
    data['time'] = activity.activity_time.strftime("%Y-%m-%d %H:%M:%S")
    data['end_time'] = activity.activity_end_time.strftime("%Y-%m-%d %H:%M:%S")

    data['type'] = activity.activity_type
    data['rule'] = activity.activity_rule
    data['form'] = activity.activity_form
    data['description'] = activity.activity_description
    data['prize'] = activity.activity_prize
    data['users_number'] = activity.activity_users_number
    data['activity_status'] = activity.activity_status

    activity_imgs=PicA.query.filter(PicA.activity==activity.activity_id).all()
    print(activity_imgs)
    img_list=(activity_imgs)
    print('img_list')
    print(img_list)
    ail = activity.activity_img_list
    print(ail)
    if (ail != None):
        ail = ail.split("'")[1::2]
        # ail = ail.split("'")
        print(ail)

    data['activity_img_list'] = ail
    pics = PicA.query.filter(PicA.activity == aid).all()
    # print(pics)
    pic_list = []
    for pic in pics:
        url = pic.url
        print(url)
        pic_list.append(url)
    data["img_list"] = pic_list

    users = activity.users
    u_num = len(users)
    data['users_attend_number'] = u_num
    print(data)

    ticket=Ticket.query.filter(Ticket.activity_id==aid).all()

    ticket_data={}
    i=0
    for ticket_item in ticket:

        ticket_item_flag={}
        ticket_item_flag['user_name']=User.query.filter(User.user_id==ticket_item.user_id).first().name
        ticket_item_flag['ticket_name']=ticket_item.name
        ticket_item_flag['ticket_time']=ticket_item.get_time.strftime("%Y-%m-%d ")

        ticket_data[str(i)]=ticket_item_flag
        i=i+1

    data['ticket']=ticket_data
    if('user_id' in dict):
        uid = dict['user_id']
        user_attend_activity = user_activity_class.query.filter(user_activity_class.user_id == uid,
                                                                user_activity_class.activity_id == aid).first()
        # print(aid)
        if user_attend_activity != None:
            data['user_activity_status']=user_attend_activity.user_activity_status
            has_attend = 1
            print('attend')
        print(user_attend_activity)
        data['user_has_attend'] = has_attend
        print('yes')

    else:
        print('None')


    return data


# @app.route('/api/activity/pic', methods=['GET'])
# def activity_pic_get():
#     """
#     返回 活动的所有图片和视频  数组
#     :return:
#     """
#     r = request.get_data()
#     dict = json.loads(r)  # 重新编码
#     aid = dict['activity']
#     print("aid = ", aid)
#     pics = PicA.query.filter(PicA.activity == aid).all()
#     print(pics)
#     print(type(pics))
#     pic_list = []
#     for pic in pics:
#         url = pic.url
#         print(url)
#         pic_list.append(url)
#     #
#     data = {
#         "img_list":pic_list
#     }
#     print(data)
#     return data




@app.route('/api/activity_picture', methods=['POST'])
def activity_upload_picture():

    """
    活动上传图片
    :return:
    """
    file = request.files['file']
    aid = request.form['activity_id']
    file_url = activity_upload_save_database(file, aid)
    print(file_url)
    print(aid)
    return file_url

@app.route('/api/activity_market', methods=['POST','GET'])
def activity_market():
    r = request.get_data()
    dict = json.loads(r)  # 重新编码
    print(dict)
    market_l = Market.query.filter(Market.area == dict['area']).all()
    print(market_l)
    market_list={}
    i = 0
    for market in market_l:
        data={}
        data['name']=market.name
        data['address']=market.address
        data['province']=market.province
        data['city']=market.city
        market_list[str(i)]=data
        i=i+1
    print(market_list)
    return market_list

#活动参与情况，所有用户的上传结果
@app.route('/api/activity_result', methods=['POST'])
def activity_result():
    """
    返回活动参与的结果
    :return:
    """
    r = request.get_data()
    dict = json.loads(r)  # 重新编码
    aid = dict['activity_id']
    print("aid = ", aid)
    users = user_activity_class.query.filter(
         user_activity_class.activity_id == aid
    ).all()
    print(users)
    i=0
    activity_result = {}
    for user in users:
        data={}
        data['user_name']=user.user_name
        data['attend_date']=user.attend_date.strftime("%Y-%m-%d")
        data['comment']=user.comment
        data['avatar']=User.query.filter(User.user_id==user.user_id).first().img_url
        pics = PicU.query.filter(
            PicU.user == user.user_id, PicU.activity == aid
        ).all()
        print(pics)
        pic_list = []
        j=0
        for pic in pics:
            url = pic.url
            print(url)
            pic_list.append(url)
            j=j+1
            if(j==9):
                break
        data['pictrue_list']=pic_list
        data['user_activity_status']=user.user_activity_status
        data['feedback_message'] = user.feedback_message
        data['production_rate']=user.production_rate
        data['booth_rate'] = user.booth_rate
        data['service_rate'] = user.service_rate
        data['activity_rate'] = user.activity_rate
        activity_result[str(i)]=data
        i=i+1
    print(activity_result)
    data = activity_result
    print(data)
    return data

@app.route('/api/activity_poster', methods=['POST','GET'])
def activity_poster():

    print(dict)
    activity = Activity.query.filter().order_by(Activity.activity_time.desc()).all()
    print(activity)
    poster_list={}
    i = 0
    for item in activity:
        data={}
        print(item.img_url)
        poster_list[item.activity_id] = item.img_url


    return poster_list