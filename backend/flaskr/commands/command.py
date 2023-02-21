'''
flask 命令 注册
flask initdb
flask hello
'''

import click

from flaskr import app, db
from flaskr.Models.models import User, Coupon, Activity, NFT
# from flaskr.Models.middle import PicA,PicU,user_activity_class


@app.cli.command("create")
def create():
    click.echo("create !")

# 以下为若干command
# @app.shell_context_processor
# def make_shell_context():
#     return dict(db=db,
#                 User=User,
#                 Activity=Activity,
#                 Coupon=Coupon,
#                 NFT=NFT,
#                 )

@app.cli.command("hello")  # 注册为命令
def hello():
    click.echo("Hello World !")

@app.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    # if drop:
    #     db.drop_all()
    #     click.echo("数据库清除!")

    db.drop_all()
    click.echo("数据库清除!")

    db.create_all()
    click.echo("初始化数据库!")

# @app.cli.command()
# def forge1():
#     # 用户 活动数据构建
#     name = "Log1c"
#     openid = "logic_openid"
#     alias = "add398"
#     img = "http://127.0.0.1:5000/static/user/logic.jpg"
#     u1 = User(name=name, open_id=openid, alias=alias, img_url=img)
#     name = "Test"
#     openid = "test_opendid"
#     u2 = User(name=name, open_id=openid, alias="test")
#
#     name = "辽沈战役  活动"
#     area = "哈尔滨"
#     a1 = Activity(activity_name=name, activity_area=area)
#
#     name = "淮海战役  活动"
#     area = "安徽"
#     a2 = Activity(activity_name=name, activity_area=area)
#
#     name = "平津战役  活动"
#     area = "北京"
#     a3 = Activity(activity_name=name, activity_area=area)
#
#     name = "多啦a梦   活动"
#     a4 = Activity(activity_name=name)
#
#     name = "萌宠趴"
#     area = "上海"
#     type = "活动"
#     des = "长城汽车 欧拉好猫乐活局"
#     time = "2021-08-08 20:00:00"
#     img_url = "http://127.0.0.1:5000/static/activity/cat_car.jpg"
#     a5 = Activity(activity_name=name,
#                   activity_area=area,
#                   activity_type=type,
#                   activity_description=des,
#                   img_url=img_url,
#                   activity_time=time)
#
#     db.session.add(u1)
#     db.session.add(u2)
#     db.session.add(a1)
#     db.session.add(a2)
#     db.session.add(a3)
#     db.session.add(a4)
#     db.session.add(a5)
#
#     db.session.commit()
#
#     click.echo('数据创建完成!')
#
#
# @app.cli.command()
# def forge2():
#     # 用户 活动 关系构建
#     u1 = User.query.filter(User.name == "Log1c").first()
#     print(u1.name)
#     u2 = User.query.filter(User.name == "Test").first()
#     print(u2)
#     a1 = Activity.query.filter(Activity.activity_id == 1).first()
#     a2 = Activity.query.filter(Activity.activity_id == 2).first()
#     a3 = Activity.query.get(3)
#     a4 = Activity.query.get(4)
#     a5 = Activity.query.get(5)
#     print(a1)
#     print(a2)
#     print(a3)
#     print(a4)
#     print(a5)
#
#     u1.activities.append(a1)
#     u1.activities.append(a2)
#     u2.activities.append(a3)
#     u2.activities.append(a4)
#
#     a1.users.append(u2)
#     a2.users.append(u2)
#     a3.users.append(u1)
#
#     u1.activities.append(a5)
#     a5.users.append(u2)
#
#     db.session.commit()
#
#     num1 = len(u1.activities)
#     num2 = len(u2.activities)
#     u1.activities_num = num1
#     u2.activities_num = num2
#
#     db.session.commit()
#
#     print(len(u1.activities))
#     print(u1.activities)
#
#     print(len(u2.activities))
#     print(u2.activities)
#
#     click.echo('建立用户————活动关系')
#
#
# @app.cli.command()
# def forge3():
#     # 优惠券 信息 添加
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
#     click.echo('优惠券 c1,c2,c3,c4已经加入数据库.')
#
#
# @app.cli.command()
# def forge4():
#     # 用户 优惠券 关系添加
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
#     click.echo('建立用户，优惠券关系')
#
#
# @app.cli.command()
# def forge5():
#     # nft 数据
#     id = 8888
#     name = "敦煌幸运飞天皮肤"
#     price = 9.99
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
#     click.echo('NFT添加进入数据库')
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
#     click.echo('NFT,用户关系建立')
#     print('nft 用户关系建立')
