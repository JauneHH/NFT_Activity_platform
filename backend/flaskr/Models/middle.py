from flaskr import db
import datetime



# 中间表 PicA ， PicU ， 活动用户表
class PicA(db.Model):
    """
    活动图片  activity picture
    """
    __tablename__ = 'pica'
    id = db.Column(db.Integer, primary_key=True)
    activity = db.Column(db.Integer, index=True)
    url = db.Column(db.String(200))

    def __repr__(self):
        return '<PicA {} >'.format(self.url)


class PicU(db.Model):
    """
    用户上传的图片   User picture
    """
    __tablename__ = 'picu'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, index=True)
    activity = db.Column(db.Integer, index=True)
    type = db.Column(db.String(100))
    url = db.Column(db.String(200))

    def __repr__(self):
        return '<PicU {} >'.format(self.url)


class user_activity_class(db.Model):
    """
        用户 活动 中间表
    """
    __tablename__ = 'user_activity_class'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    user_name = db.Column(db.String(40))
    activity_id = db.Column(db.Integer)
    activity_name = db.Column(db.String(40))

    user_activity_status = db.Column(db.Integer, default=0)
    comment = db.Column(db.String(100))  # 用户评论活动
    attend_date = db.Column(db.Date, default=datetime.date.today()) # 用户参与活动的日期，默认即可
    city = db.Column(db.String(20),default="上海")
    male = db.Column(db.Integer,default=1) # 男为1，女为0
    address = db.Column(db.String(10))
    feedback_message = db.Column(db.String(200))#平台反馈信息
    has_read=db.Column(db.Integer)#是否已读
    ticket = db.Column(db.Integer,default=0)  # 是否发送电影票
    production_rate=db.Column(db.Float)#产品打分
    booth_rate = db.Column(db.Float)  # 展台打分
    service_rate = db.Column(db.Float)  # 服务打分
    activity_rate = db.Column(db.Float)  # 活动打分

    def __repr__(self):
        return '<user_activity_class {} , {} , {}，{}>'.format(
            self.user_name, self.activity_name, self.user_activity_status, self.comment)
