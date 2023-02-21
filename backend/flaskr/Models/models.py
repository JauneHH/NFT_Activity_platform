import datetime

from flaskr import db

# 活动和用户 多对多
# 活动和优惠券 一对多
# 用户和优惠券 多对多
# 用户 NFT 多对多

# 用户活动中间表
user_activity_table = db.Table('user_activity',
                               db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')),
                               db.Column('user_name', db.String(40)),
                               db.Column('activity_id', db.Integer, db.ForeignKey('activity.activity_id')),
                               db.Column('activity_name', db.String(40)),

                               )

# 用户优惠券中间表
user_coupon_table = db.Table('user_coupon',
                             db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')),
                             db.Column('user_name', db.String(40)),
                             db.Column('coupon_id', db.Integer, db.ForeignKey('coupon.coupon_id')),
                             db.Column('coupon_name', db.String(40)),
                             )



class user_NFT_table(db.Model):
    __tablename__ = "user_nft_table"
    id = db.Column(db.Integer, primary_key=True)  # 主键，自动生成

    user_id = db.Column(db.Integer)  # 主键，自动生成
    user_name = db.Column(db.String(40))  # 用户name，自动生成
    NFT_id = db.Column(db.Integer)  # NFTid，自动生成
    NFT_name = db.Column(db.String(40))  # NFTname，自动生成
    privateKey=db.Column(db.String(200))#私钥
    signature=db.Column(db.String(200))#签名
    transaction_time = db.Column(db.DateTime)

    def __repr__(self):
        return '<user_NFT_table {} >'.format(self.id)

    __str__ = __repr__

class User(db.Model):
    """
    用户表
    """
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)  # 主键，自动生成
    name = db.Column(db.String(40))
    alias = db.Column(db.String(40))  # 用户昵称
    img_url = db.Column(db.String(200))  # 头像url  face_src
    open_id = db.Column(db.String(40), unique=True)  # 用户唯一标志
    city = db.Column(db.String(30)) # 用户来自的城市
    male = db.Column(db.Integer,default=1)  # 1 为男，0为女
    photographer = db.Column(db.Integer, default=0)  # 是否为摄影师，1 为是，0为否，默认否
    private_key=db.Column(db.String(100))#私钥
    public_key=db.Column(db.String(100))#公钥
    # 加个签名

    activities = db.relationship('Activity',
                                 secondary=user_activity_table,
                                 backref=db.backref('users')
                                 )
    activities_num = db.Column(db.Integer)  # 活动数目

    coupons = db.relationship('Coupon',
                              secondary=user_coupon_table,
                              backref=db.backref('users')
                              )
    coupons_num = db.Column(db.Integer)  # 优惠券数量
    point = db.Column(db.Integer,default=0)  # 优惠券数量

    nfts_num = db.Column(db.Integer)  # nft 数量

    def __repr__(self):
        return '<User {} >'.format(self.name)

    __str__ = __repr__


class Activity(db.Model):
    """
    活动表
    """
    __tablename__ = "activity"
    activity_id = db.Column(db.Integer, primary_key=True)  # 主键，自动生成
    activity_name = db.Column(db.String(40))

    activity_description = db.Column(db.String(400),default="活动描述")  # 描述
    activity_prize = db.Column(db.String(400),default="活动奖励")
    activity_rule = db.Column(db.String(400),default="活动规则")
    activity_form = db.Column(db.String(200),default="活动形式")

    activity_area = db.Column(db.String(50), default="上海")  # 地点
    img_url = db.Column(db.String(200), default="")  # 图片URL
    activity_type = db.Column(db.String(50), default="电影")  # 活动类型
    activity_status = db.Column(db.Integer,default=0)   # 活动是否还在持续

    comment_img = db.Column(db.String(200),default="还未生成词云图片") # 词云图片
    activity_text1 = db.Column(db.String(400))
    # activity_text2 = db.Column(db.String(400))
    # activity_text3 = db.Column(db.String(400))
    # Date
    activity_time = db.Column(db.DateTime, default=datetime.datetime.now)
    activity_end_time = db.Column(db.DateTime, default=datetime.datetime.now)

    coupons = db.relationship("Coupon", backref="activity")
    activity_users_number = db.Column(db.Integer)  # 活动参加人数

    activity_img_list = db.Column(db.String(400))

    def __repr__(self):
        return '<Activity {} >'.format(self.activity_name)


class Coupon(db.Model):
    """
    优惠券
    """
    __tablename__ = "coupon"
    coupon_id = db.Column(db.Integer, primary_key=True)  # 主键，自动生成
    coupon_name = db.Column(db.String(40))
    coupon_description = db.Column(db.String(400))
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.activity_id'))  # 外键

    def __repr__(self):
        return '<Coupon {} >'.format(self.coupon_name)


class NFT(db.Model):
    """
    NFT
    """
    __tablename__ = 'nft'
    NFT_id = db.Column(db.Integer, primary_key=True)
    NFT_name = db.Column(db.String(40))
    NFT_price = db.Column(db.Float)
    NFT_description = db.Column(db.String(400), default="NFT数字作品")
    NFT_time = db.Column(db.DateTime, default=datetime.datetime.now)
    img_url = db.Column(db.String(200))  # 图像 url  NFT_src
    QRcode_url = db.Column(db.String(200))# 二维码 url  NFT_src
    publicKey=db.Column(db.String(200))#公钥
    creator=db.Column(db.String(50))#创作者
    owner = db.Column(db.String(50))  # 拥有者
    address= db.Column(db.String(100))  # 地址
    transection_time = db.Column(db.DateTime, default=datetime.datetime.now)


    def __repr__(self):
        return '<NFT {} >'.format(self.NFT_id)


class Ticket(db.Model):
    """电影票"""
    __tablename__ = 'ticket'
    id = db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer)
    ticket_type = db.Column(db.Integer)
    url = db.Column(db.String(200))
    name = db.Column(db.String(40))
    exchange_code = db.Column(db.String(50))
    password = db.Column(db.String(50))
    has_receive = db.Column(db.Integer,default=0)
    activity_id = db.Column(db.Integer)
    get_time=db.Column(db.DateTime)
    def __repr__(self):
        return '<Ticket {} >'.format(self.name)

class Market(db.Model):
    """商场"""
    __tablename__ = 'market'
    id = db.Column(db.Integer, primary_key=True)
    province = db.Column(db.String(10))
    city = db.Column(db.String(10))
    area=db.Column(db.String(10))
    name = db.Column(db.String(30))
    address=db.Column(db.String(100))

    def __repr__(self):
        return '<Market {} >'.format(self.name)

class User_activity_replace(db.Model):
        """用户回复"""
        __tablename__ = 'User_activity_replace'
        id = db.Column(db.Integer, primary_key=True)
        province = db.Column(db.String(10))
        city = db.Column(db.String(10))
        area = db.Column(db.String(10))
        name = db.Column(db.String(30))
        address = db.Column(db.String(100))

        def __repr__(self):
            return '<User_activity_replace {} >'.format(self.name)


class User_activity_message(db.Model):
    """用户回复"""
    __tablename__ = 'User_activity_message'
    id = db.Column(db.Integer, primary_key=True)
    activity_id=db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    feedback_message = db.Column(db.String(200))#平台反馈信息
    has_read=db.Column(db.Integer,default=0)#是否已读
    ticket = db.Column(db.Integer,default=0)  # 是否发送电影票
    time=db.Column(db.DateTime)#时间
    ticket_name = db.Column(db.String(100))  # 电影票名称
    user_activity_status = db.Column(db.Integer)  #审核信息状态
    NFT_name = db.Column(db.String(50))  # NFT名称
    NFT_url = db.Column(db.String(200))  # NFT名称
    def __repr__(self):
        return '<User_activity_message {} >'.format(self.id)
