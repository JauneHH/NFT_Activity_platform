from flaskr import db
from flaskr.Models.models import User, Coupon, Activity, NFT
from flaskr.Models.middle import user_activity_class, PicU, PicA


def forge1():
    """
    用户  测试数据构建
    """
    name = "Log1c"
    openid = "logic_openid"
    alias = "add398"
    city = "上海"
    male = 1
    # img = "http://127.0.0.1:5000/static/user/logic.jpg"
    u1 = User(name=name, open_id=openid, alias=alias,city = city, male = male)
    db.session.add(u1)

    for i in range(7):
        name1 = name + str(i)
        openid1 = openid + str(i)
        alias1 = alias + str(i)
        city1 = city
        male1 = male
        u = User(
            name = name1,
            open_id = openid1,
            alias = alias1,
            city = city1,
            male = male1
        )
        db.session.add(u)

    name = "小意"
    openid = "xiaoyi"
    alias = "s"
    city = "上海"
    male = 0
    u = User(
        name=name,
        open_id=openid,
        alias=alias,
        city=city,
        male=male
    )
    db.session.add(u)

    for i in range(5):
        name1 = name + str(i)
        openid1 = openid + str(i)
        alias1 = alias + str(i)
        city1 = city
        male1 = 0
        u = User(
            name=name1,
            open_id=openid1,
            alias=alias1,
            city=city1,
            male=male1
        )
        db.session.add(u)

    name = "test1"
    city = "北京"
    male = 1
    u = User(
        name=name,
        city=city,
        male=male
    )
    db.session.add(u)

    name = "test2"
    city = "北京"
    male = 0
    u = User(
        name=name,
        city=city,
        male=male
    )
    db.session.add(u)

    name = "test3"
    city = "北京"
    male = 1
    u = User(
        name=name,
        city=city,
        male=male
    )
    db.session.add(u)

    name = "test4"
    city = "安徽"
    male = 1
    u = User(
        name=name,
        city=city,
        male=male
    )
    db.session.add(u)

    name = "test5"
    city = "安徽"
    male = 0
    u = User(
        name=name,
        city=city,
        male=male
    )
    db.session.add(u)
    db.session.commit()
    print('用户数据创建完成!')


def forge2():
    name = "创意猫咪市集"
    area = "北京"
    a1 = Activity(
        activity_name=name,
        activity_area=area,
        activity_time = "2021-12-4 14:00:00",
        activity_users_number=20,
        activity_description='为在欧拉体验店参与欧拉猫咪市集,活动的顾客拍摄打卡照片并制作个人独家NFT照片海报，同时赠送电影票1张',
        activity_prize='个人独家NFT照片海报，同时赠送电影票1张',
        activity_form='线下打卡互动体验留影活动',
        activity_rule='为在欧拉体验店参与欧拉猫咪市集 活动的顾客拍摄打卡照片并制作个人独家NFT 照片海报，同时赠送电影票1张',
    )


    db.session.add(a1)
    db.session.commit()
    print("电影数据创建完成!")


def forge3():
    print('null')


def forge4():
    urls = [
        "http://127.0.0.1:5000/_uploads/files/user/6/logic.jpg",
        "http://127.0.0.1:5000/_uploads/files/user/6/origin_202109221742405975.jpg",
        "http://127.0.0.1:5000/_uploads/files/user/6/origin_202108171857357210.jpg",
        "http://127.0.0.1:5000/_uploads/files/user/6/origin_202107091442465671.jpg",
        "http://127.0.0.1:5000/_uploads/files/user/9/logic.jpg",
        "http://127.0.0.1:5000/_uploads/files/user/9/origin_202109221742405975.jpg",
        "http://127.0.0.1:5000/_uploads/files/user/9/origin_202108171857357210.jpg",
        "http://127.0.0.1:5000/_uploads/files/user/9/origin_202107091442465671.jpg"
    ]
    for i in range(4):

        uid = 6
        aid = 1
        url = urls[i]
        p = PicU(
            user=uid,
            activity=aid,
            url=url
        )
        db.session.add(p)

    for i in range(4,8):
        uid = 9
        aid = 1
        url = urls[i]
        p = PicU(
            user=uid,
            activity=aid,
            url=url
        )
        db.session.add(p)
    db.session.commit()
    print("图片已经上传")


def forge5():
    urls = [
        "http://127.0.0.1:5000/_uploads/files/activity/1/09e41c9d7d175a90aa5d4e9f1c62ce5d.gif",
        "http://127.0.0.1:5000/_uploads/files/activity/1/origin_202109200910571795.gif",
        "http://127.0.0.1:5000/_uploads/files/activity/1/image001.jpeg"
        ]
    aid = 1
    for i in range(3):
        url = urls[i]
        pica = PicA(activity = aid,url = url)
        db.session.add(pica)
    db.session.commit()
    print("活动图片以上传")


#
# def forge3_1():
#     """
#     优惠券 信息 添加
#     """
#     c1 = Coupon(coupon_name="activity1——c1",
#                 coupon_description="100%",
#                 activity_id=1
#                 )
#     c2 = Coupon(coupon_name="activity1——c2",
#                 coupon_description="50%",
#                 activity_id=1
#                 )
#
#     c3 = Coupon(coupon_name="activity2——c3",
#                 coupon_description="100%",
#                 activity_id=2
#                 )
#
#     c4 = Coupon(coupon_name="activity2——c4",
#                 coupon_description="50%",
#                 activity_id=2
#                 )
#
#     db.session.add(c1)
#     db.session.add(c2)
#     db.session.add(c3)
#     db.session.add(c4)
#
#     db.session.commit()
#     print(c1, c2, c3, c4)
#     print('优惠券 c1,c2,c3,c4已经加入数据库.')
#
#
# def forge3_2():
#     """
#     # 用户 优惠券 关系添加
#     """
#     u1 = User.query.get(1)
#     print(u1)
#
#     c1 = Coupon.query.get(1)
#     print(c1)
#     c2 = Coupon.query.get(2)
#     print(c2)
#     c3 = Coupon.query.get(3)
#     print(c3)
#     c4 = Coupon.query.get(4)
#     print(c4)
#
#     u1.coupons.append(c1)
#     u1.coupons.append(c2)
#     u1.coupons.append(c3)
#     u1.coupons.append(c4)
#
#     db.session.commit()
#
#     print(u1.coupons)
#     l = len(u1.coupons)
#     u1.coupons_num = l
#
#     db.session.commit()
#     print(u1.coupons_num)
#
#     print('建立用户，优惠券关系')
#
#
# def forge5():
#     """
#     nft 数据
#     """
#
#     name = "敦煌幸运飞天皮肤"
#     price = 9.99
#     id = 8888
#     des = '权益介绍，需要支付宝实名认证以后才能成功兑换NFT数字作品'
#     n1 = NFT(NFT_id=id, NFT_name=name,
#              NFT_price=price,
#              NFT_description=des
#              )
#     n2 = NFT(NFT_id=8000, NFT_name=name,
#              NFT_price=price,
#              NFT_description=des
#              )
#
#     db.session.add(n1)
#     db.session.add(n2)
#     db.session.commit()
#     print(n1)
#     print(n2)
#     print('NFT添加进入数据库')
#
#     u1 = User.query.filter(User.name == "Log1c").first()
#     print(u1.name)
#     u2 = User.query.filter(User.name == "Test").first()
#     print(u2)
#
#     u1.nfts.append(n1)
#     u1.nfts.append(n2)
#     n1.users.append(u2)
#     db.session.commit()
#     print('NFT,用户关系建立')
#     print('nft 用户关系建立')
