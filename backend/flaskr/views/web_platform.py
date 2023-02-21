"""
user
用户相关
"""
import json

import requests
from flask import request
from flask import render_template
from flaskr import app, db
from flaskr.Models.models import User, Activity
from flaskr.Models.middle import PicU, user_activity_class
from flaskr.views.upload import user_upload_save_database


@app.route('/activity', methods=['GET', 'POST'])
def activity():
    return render_template('activity.html')

@app.route('/manage_platform', methods=['GET', 'POST'])
def test():
    picu=PicU.query.filter().all()
    for item in picu:
        img_id = item.url.split('.')[-1]

        if (img_id != "bmp" and img_id != "png" and img_id != "gif" and img_id != "jpg" and img_id != "jpeg"):
            item.type='video'
        else:
            item.type='image'
        db.session.commit()

    the_news = {
        'XXX1': '1',
        'XXX2': '2',
        'XXX3': '3',
        'XXX4': '4',
    }
    context = {
        'title': '新闻',
        'the_news': the_news,
    }
    return render_template('test.html',context=context)

@app.route('/user_activity_url', methods=['GET', 'POST'])
def user_activity_url():

    return render_template('user_activity_url.html')

@app.route('/publish_activity', methods=['GET', 'POST'])
def publish_activity():

    return render_template('publish_activity.html')

@app.route('/user', methods=['GET', 'POST'])
def user():

    return render_template('user.html')

@app.route('/api/indexh5', methods=['GET', 'POST'])
def indexh5():
    return render_template('pages/test_element/index.html')


@app.route('/activity_statistics', methods=['GET', 'POST'])
def activity_statistics():

    return render_template('activity_statistics.html')

@app.route('/activity_statistics_item', methods=['GET', 'POST'])
def activity_statistics_item():

    return render_template('activity_statistics_item.html')
@app.route('/user_prize', methods=['GET', 'POST'])
def user_prize():

    return render_template('user_prize.html')
@app.route('/user_prize_item', methods=['GET', 'POST'])
def user_prize_item():

    return render_template('user_prize_item.html')

@app.route('/ziptest', methods=['GET', 'POST'])
def ziptest():

    return render_template('ziptest.html')

@app.route('/NFT', methods=['GET', 'POST'])
def NFT():

    return render_template('NFT.html')

@app.route('/NFT_user', methods=['GET', 'POST'])
def NFT_user():

    return render_template('NFT_user.html')

