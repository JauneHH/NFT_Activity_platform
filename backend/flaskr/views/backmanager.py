from flask import request
import json
import datetime
from flaskr import app, db, files
from flaskr.Models.middle import PicU, user_activity_class,PicA
from flaskr.Models.models import Activity,User,Ticket,User_activity_message,NFT,user_NFT_table
from flaskr.views.server_specialized import NFT_File, bytes2hex, hex2bytes
from flaskr.views.server_type_2 import NFT_creator


@app.route('/api/manager/activity_list', methods=['POST'])
def manager_activity_list():
    """
    1. 活动列表
    后台管理获取当前活动列表
    :return:
    """
    activities = Activity.query.all()

    print(activities)
    l = len(activities)
    print(l)
    data = []
    Datetime=datetime.datetime.now()
    print(Datetime)

    for i in range(l):
        act = activities[i]
        if (act.activity_status==0):
            if (Datetime > act.activity_time and Datetime < act.activity_end_time):
                act.activity_status = 1
                activity_status = 1
        if (Datetime > act.activity_end_time):
            act.activity_status = 2


        d = {
            'activity_id': act.activity_id,
            'activity_name': act.activity_name,
            'activity_area': act.activity_area,
            'activity_time': act.activity_time.strftime("%Y-%m-%d %H:%M:%S"),
            'activity_end_time': act.activity_end_time.strftime("%Y-%m-%d %H:%M:%S"),
            'activity_type': act.activity_type,
            'activity_status': act.activity_status,
            'img_url': act.img_url,
            'activity_prize': act.activity_prize,
            'activity_rule': act.activity_rule,
            'activity_description': act.activity_description,
            'activity_form': act.activity_form,
            'activity_users_number': act.activity_users_number
        }
        data.append(d)
    db.session.commit()
    result = {'msg': data}
    print(result)
    return result


@app.route('/api/manager/activity_publish', methods=['POST'])
def manager_activity_publish():
    """
    2. 发布活动
    :return:
    """
    activity_img_list = []
    print(request.files)
    print(request.form)
    # #poster = request.files['file1']
    # # print(request.files['file'])
    # #filename = files.save(poster, 'poster')
    # #poster_url = files.url(filename)
    # activity_img_list.append(poster_url)
    # print(poster_url)
    poster_url=''
    for item in request.files:
        print(item)
        print(request.files[item])
        file = request.files[item]
        # if file == poster:
        #     print("不能再保存这一张图")
        #     continue
        filename1 = files.save(file, 'video')
        file_url = files.url(filename1)
        if(item=='file_poster'):
            poster_url=file_url
        else:
            activity_img_list.append(file_url)
    print(activity_img_list)

    activity_name = request.form['activity_name']
    activity_area = request.form['activity_area']
    print("1")
    activity_time = datetime.datetime.strptime(request.form['activity_time'], "%Y-%m-%d %H:%M:%S")
    activity_end_time = datetime.datetime.strptime(request.form['activity_end_time'], "%Y-%m-%d %H:%M:%S")
    activity_type = request.form['activity_type']
    activity_users_number = request.form['activity_users_number']
    activity_description = request.form['activity_description']
    activity_form = request.form['activity_form']
    activity_prize = request.form['activity_prize']
    activity_rule = request.form['activity_rule']
    # activity_status = request.form['activity_status']
    # activity_img_list = request.form['activity_img_list']
    print("1111")

    a = Activity(
        activity_name=activity_name,
        img_url = poster_url,
        activity_description=activity_description,
        activity_area=activity_area,
        activity_time=activity_time,
        activity_end_time=activity_end_time,
        activity_type=activity_type,
        activity_users_number=activity_users_number,
        activity_rule=activity_rule,
        activity_prize=activity_prize,
        activity_status=0,
        activity_form=activity_form,
        activity_img_list=str(activity_img_list)
    )
    db.session.add(a)

    db.session.commit()
    print(a.activity_id)
    for item in activity_img_list:
        print(item)
        pica=PicA(activity=a.activity_id,
                  url=str(item)
        )
        db.session.add(pica)

    db.session.commit()
    return "已添加活动"


@app.route('/api/manager/activity_user_list', methods=['POST'])
def manager_activity_user_list():
    """
    3. 各个活动所参与的用户列表
    :return:
    """
    r = request.get_data()
    print(r)
    dict = json.loads(r)  # 重新编码
    print(dict)
    aid = dict
    print(aid)
    a = Activity.query.get(aid)
    print(a)
    users = a.users
    print(users)
    count = len(users)
    print(count)
    data = []
    for i in range(count):
        user = users[i]
        uid = user.user_id
        uac = user_activity_class.query.filter(
            user_activity_class.user_id == uid,
            user_activity_class.activity_id == aid
        ).first()

        pics = PicU.query.filter(
            PicU.user == uid, PicU.activity == aid
        ).all()
        ticket_item=Ticket.query.filter(
            Ticket.user_id==uid,Ticket.activity_id==aid
        ).all()
        ticket_number=0
        for ticket in ticket_item:
            ticket_number=ticket_number+1
        uac.ticket=ticket_number
        print(pics)
        pic_list = []
        video_list=[]
        for pic in pics:
            if(pic.type=='image'):
                url = pic.url
                print(url)
                pic_list.append(url)


            else:
                url = pic.url
                print(url)
                video_list.append(url)

        data_img_list = {
            "img_list": pic_list
        }
        d = {
            "user_id": user.user_id,
            "user_name": user.name,
            "alias": user.alias,
            "img_url": user.img_url,
            'comment':uac.comment,
            "user_activity_status": uac.user_activity_status,
            "img_list":pic_list,
            "video_list": video_list,
            "feedback_message":uac.feedback_message,
            'ticket':ticket_number,
            "production_rate":uac.production_rate,
            "booth_rate":uac.booth_rate,
            "service_rate":uac.service_rate,
            "activity_rate":uac.activity_rate

        }
        data.append(d)
    print(data)
    result = {'msg': data}
    return result


@app.route('/api/manager/activity_user_uploadInformation', methods=['POST'])
def activity_user_uploadInformation():
    """
    4. 用户上传的信息
    获取用户对应所参与活动上传的信息
    :return:
    """
    uid = request.form['user_id']
    print(uid)
    aid = request.form['activity_id']
    print(aid)

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
        "img_list": pic_list
    }
    return data


@app.route('/api/manager/activity_statistics', methods=['POST'])
def activity_last_statistics():
    """
    5. 各个活动的最后数据
    获取用户对应所参与活动上传的信息
    :return:
    """
    print(request)
    aid = request.form['activity_id']
    print(aid, 'activity_id')
    uacs = user_activity_class.query.filter(
        user_activity_class.activity_id == aid
    ).all()


    print(len(uacs))

    attend_date = []  # 检查是否存在某日期
    user_attend_date = []
    for uac in uacs:
        date = uac.attend_date
        date = date.strftime("%Y-%m-%d")
        print(date)
        gender = uac.male
        if date not in attend_date:
            attend_date.append(date)
            dmf = {}
            dmf["date"] = date
            dmf["male"] = 0
            dmf["female"] = 0
            dmf["total"] = 1
            if gender == 1:
                dmf["male"] += 1
            else:
                dmf["female"] += 1
            user_attend_date.append(dmf)

        else:  # date in attend_date
            for d in user_attend_date:
                if date == d["date"]:
                    d["total"] += 1
                    if gender == 1:
                        d["male"] += 1
                    else:
                        d["female"] += 1
                    break

    print(user_attend_date)
    max_total=0
    for date_item in user_attend_date:

        if(date_item['total']>max_total):
            max_total=date_item['total']


    user_areas = []
    city_list = []  # 是否存在某个城市
    for uac in uacs:
        city = uac.city
        if city not in city_list:
            city_list.append(city)
            an = {}
            an["name"] = city
            an["value"] = 1
            user_areas.append(an)

        else:  # city in city_list
            for a in user_areas:
                if a["name"] == city:
                    a["value"] += 1
                    break

    picus = PicU.query.filter(PicU.activity == aid).limit(10).all()
    print(picus)
    print(len(picus))
    print(type(picus))
    img_list = []
    for picu in picus:
        img_list.append(picu.url)
    print(img_list)
    pic_list = []
    video_list = []
    for pic in picus:
        if (pic.type == 'image'):
            url = pic.url
            print(url)
            pic_list.append(url)

        else:
            url = pic.url
            print(url)
            video_list.append(url)

    a1 = Activity.query.filter(Activity.activity_id == aid).first()
    comment_img = a1.comment_img
    print(comment_img)

    uac = user_activity_class.query.filter(
        user_activity_class.activity_id == aid
    ).all()

    user_activity_statistics_data=[]
    for uac_item in uac:
        user=User.query.filter(User.user_id==uac_item.user_id).first()
        ticket=Ticket.query.filter(Ticket.user_id==uac_item.user_id,Ticket.activity_id==aid).all()
        ticket_number=0
        for ticket_item in ticket:
            ticket_number=ticket_number+1
        data_item={}
        data_item['activity_name'] = uac_item.activity_name
        data_item['user_name'] = uac_item.user_name
        data_item['user_attend_date'] = uac_item.attend_date.strftime("%Y-%m-%d")
        if(uac_item.user_activity_status==0):
            data_item['user_activity_status'] ='待参加'
        elif(uac_item.user_activity_status==1):
            data_item['user_activity_status'] = '待审核'
        elif (uac_item.user_activity_status == 2):
            data_item['user_activity_status'] = '审核未通过'
        elif (uac_item.user_activity_status == 3):
            data_item['user_activity_status'] = '审核通过'
        elif (uac_item.user_activity_status == 4):
            data_item['user_activity_status'] = '审核通过'


        data_item['ticket_name'] = '电影票'
        data_item['ticket_number'] = ticket_number
        if ticket_number==0:
            data_item['ticket_status'] = '未发放'
        else:
            data_item['ticket_status'] = '已发放'
        data_item['production_rate'] = uac_item.production_rate
        data_item['booth_rate'] = uac_item.booth_rate
        data_item['service_rate'] = uac_item.service_rate
        data_item['activity_rate'] = uac_item.activity_rate
        data_item['point'] = user.point
        user_activity_statistics_data.append(data_item)
    print('data',user_activity_statistics_data)

    res ={

        "user_activity_statistics":user_activity_statistics_data,
        "user_attend_date": user_attend_date,
        'max_tatal':max_total,
        "user_areas": user_areas,
        "img_list": pic_list,
        "comment_img": comment_img,
        "video_list":video_list
    }
    print(res)
    return {
        "user_activity_statistics":user_activity_statistics_data,
        "user_attend_date": user_attend_date,
        'max_tatal':max_total,
        "user_areas": user_areas,
        "img_list": pic_list,
        "comment_img": comment_img,
        "video_list":video_list
    }


@app.route('/api/manager/activity_user_status', methods=['POST'])
def activity_user_status():
    """
    6. 后台管理审核参与活动的用户是否合格
    获取用户对应所参与活动上传的信息
    :return:
    """
    print(request.form)
    aid = request.form['activity_id']
    uid = request.form['user_id']
    result = request.form['result']
    feedback_message=request.form['feedback_message']
    print(request.form)
    uac = user_activity_class.query.filter(
        user_activity_class.activity_id == aid,
        user_activity_class.user_id == uid

    ).first()

    flag=2
    if result == "1":
        print('uac')
        uac.user_activity_status = 3
        flag=3

    else:
        print('uac')
        uac.user_activity_status = 2

    uac.feedback_message=feedback_message
    message = User_activity_message(
        activity_id=aid,
        user_id=uid,
        feedback_message=feedback_message,
        time=datetime.datetime.now(),
        user_activity_status=flag
    )
    if (feedback_message != None):
        uac.has_read = 1
    db.session.add(message)
    db.session.commit()
    data = {
        "user_activity_status": uac.user_activity_status
    }
    return data


@app.route('/api/manager/activity_delete', methods=['GET', 'Post'])
def activity_delete():
    """
    7. 删除活动
    :return:
    """
    aid = request.form['activity_id']
    a = Activity.query.filter(Activity.activity_id == aid).first()
    user_activity_class.query.filter(user_activity_class.activity_id == aid).delete()
    db.session.delete(a)
    db.session.commit()
    print('delete')
    return "ok"

@app.route('/api/manager/user_photographer', methods=['GET', 'Post'])
def user_photographer():
    """
    8. 查看摄影师权限
    :return:
    """
    user=User.query.filter().all()
    Data=[]
    for item in user:
        data={}
        data['id'] = item.user_id
        data['name']=item.name
        data['img_url']=item.img_url
        data['photographer']='有权限' if item.photographer==1 else'无权限'
        Data.append(data)
    result = {'msg': Data}
    print(result)
    return result

@app.route('/api/manager/modify_user_photographer', methods=['GET', 'Post'])
def modify_user_photographer():
    """
    9. 修改摄影师权限
    :return:
    """
    print(request.form)
    uid = request.form['userid']
    user=User.query.filter(User.user_id==uid).first()
    print(user)
    user.photographer=request.form['photographer']
    db.session.commit()

    return "true"

@app.route('/api/manager/activity_user_gift', methods=['POST'])
def activity_user_gift():
    """
    10. 后台管理发放奖品
    :return:
    """
    print(request.form)
    aid = request.form['activity_id']
    uid = request.form['user_id']
    print(request.form)
    uac = user_activity_class.query.filter(
        user_activity_class.activity_id == aid,
        user_activity_class.user_id == uid

    ).first()

    uac.user_activity_status=4
    if (request.form['exchange_code'] != ''):
        print(request.form['exchange_code'])
        ticket = Ticket(
            exchange_code=request.form['exchange_code'],
            name=request.form['ticket_name'],
            user_id=uid,
            activity_id=aid,
            password=request.form['password'],
            get_time=datetime.datetime.now()
        )
        message=User_activity_message(
            activity_id=aid,
            user_id=uid,
            ticket_name=request.form['ticket_name'],
            time=datetime.datetime.now()
        )
        if(request.form['exchange_point']):
            user = User.query.filter(User.user_id == uid).first()
            user.point =user.point+int(request.form['exchange_point'])
        db.session.add(ticket)
        db.session.add(message)
        db.session.commit()

    db.session.commit()
    data = {
        "user_activity_status": uac.user_activity_status
    }
    return {'msg':'true'}

@app.route('/api/manager/pause_activity', methods=['POST'])
def pause_activity():
    """
    11. 暂停/开始活动
    :return:
    """
    print(request.form)
    aid = request.form['activity_id']
    status=request.form['activity_status']
    activity_item=Activity.query.filter(Activity.activity_id==aid).first()
    if(status=='已暂停'):
        activity_item.activity_status=1
    elif(status=='进行中'):
        activity_item.activity_status = 3
    db.session.commit()

    return {'msg':'true'}

@app.route('/api/manager/activity_user_NFT', methods=['POST'])
def activity_user_NFT():
    """
    12. 用户NFT
    :return:
    """

    r = request.get_data()
    print(r)
    dict = json.loads(r)  # 重新编码
    print(dict)
    aid = dict
    print(aid)
    a = Activity.query.get(aid)
    print(a)
    users = a.users
    print(users)
    count = len(users)
    print(count)
    data = []
    for i in range(count):
        user = users[i]
        uid = user.user_id
        uac = user_activity_class.query.filter(
            user_activity_class.user_id == uid,
            user_activity_class.activity_id == aid
        ).first()
        user=User.query.filter(User.user_id==uid).first()
        NFTs=NFT.query.filter(NFT.owner==user.name).all()

        pics = PicU.query.filter(
            PicU.user == uid, PicU.activity == aid
        ).all()
        print(pics)
        pic_list = []
        video_list = []
        NFT_url=[]
        for NFT_item in NFTs:
            NFT_url.append(NFT_item.img_url)
        for pic in pics:
            if (pic.type == 'image'):
                url = pic.url
                print(url)
                pic_list.append(url)


            else:
                url = pic.url
                print(url)
                video_list.append(url)

        data_img_list = {
            "img_list": pic_list
        }
        d = {
            "user_id": user.user_id,
            "user_name": user.name,
            "alias": user.alias,
            "img_url": user.img_url,
            'comment': uac.comment,
            "user_activity_status": uac.user_activity_status,
            "img_list": pic_list,
            "video_list": video_list,
            "feedback_message": uac.feedback_message,
            "NFT_list":NFT_url,
            "production_rate": uac.production_rate,
            "booth_rate": uac.booth_rate,
            "service_rate": uac.service_rate,
            "activity_rate": uac.activity_rate

        }
        data.append(d)
    print(data)
    result = {'msg': data}
    return result

@app.route('/api/manager/send_NFT', methods=['POST'])
def send_NFT():
    """
    13. 发放NFT
    :return:
    """
    print(request.files)
    print(request.form)
    user_id=request.form['user_id']
    user=User.query.filter(User.user_id==user_id).first()
    print(request.form)
    filename = request.files['NFT_poster'].filename
    file = request.files['NFT_poster']
    location = 'NFT/Image/'
    print("location = ", location)
    filename_url = files.save(file, location)
    print("filename = ", filename_url)
    url = files.url(filename_url)

    NFT_item_create = NFT(
        img_url=url,
        NFT_time=datetime.datetime.now(),
        NFT_name=request.form['NFT_name']
    )
    db.session.add(NFT_item_create)
    db.session.flush()
    db.session.commit()
    NFT_item=NFT.query.filter(NFT.img_url==url).first()

    #all_the_text = open('/Users/huangzexi/PycharmProjects/end_demo11.28/flaskr/static/' + filename_url,'rb').read()
    all_the_text = open('/root/myflask/flaskr/static/' + filename_url,'rb').read()

    NFT_test = NFT_creator(all_the_text)
    print(NFT_test)
    NFT_data = NFT_File(all_the_text)  # 上传文件生成签名
    print(NFT_data)

    uer_nft_item = user_NFT_table(
        NFT_id=NFT_item.NFT_id,
        user_id=user_id,
        signature=NFT_data['signature'],
        privateKey=NFT_data['privatekey'],
        user_name=user.name,
    )

    NFT_item.creator = '棒棒糖home'
    NFT_item.owner = user.name
    NFT_item.address = NFT_test['address']
    NFT_item.transection_time = NFT_item.NFT_time
    db.session.flush()
    db.session.commit()

    db.session.add(uer_nft_item)
    db.session.flush()
    db.session.commit()

    message = User_activity_message(
        activity_id=request.form['activity_id'],
        user_id=user_id,
        NFT_name=request.form['NFT_name'],
        NFT_url=url,
        time=datetime.datetime.now()
    )
    db.session.add(message)
    db.session.commit()

    return {'msg':'true'}



