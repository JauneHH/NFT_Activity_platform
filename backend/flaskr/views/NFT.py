import json
import datetime
from flask import request
import qrcode, os
from flaskr import app, files, db
from sqlalchemy import or_,and_

from flaskr.Models.models import User, NFT, user_NFT_table
from flaskr.views.server_specialized import NFT_File, bytes2hex, hex2bytes
from flaskr.views.server_type_2 import NFT_creator

""""NFT"""


@app.route('/api/NFT_list', methods=['GET', 'POST'])
def nft_list():
    # 3.1 NFT列表
    # 每个NFT数字海报的具体信息

    nfts = NFT.query.all()
    l = len(nfts)
    print(l)
    print(nfts)

    Data = {
        "num": l,
    }
    i = 0
    for nft in nfts:
        data = {}
        print(nft, "       ",
              nft.NFT_id, "        ",
              nft.NFT_name, "       ",
              nft.img_url, "        ",
              nft.NFT_time, "        ",
              )

        data['id'] = nft.NFT_id
        data['name'] = nft.NFT_name
        data['img_url'] = nft.img_url
        data['time'] = nft.NFT_time
        Data[str(i)] = data
        i = i + 1

    return Data


@app.route('/api/NFT_information', methods=['POST'])
def nft_information_get():
    # 3.2 NFT 信息
    # 每个NFT数字海报的具体信息
    r = request.get_data()
    print(r)
    dict = json.loads(r)  # 重新编码
    print(dict)

    NFT_id = dict['NFT_id']
    print(NFT_id)

    nft = NFT.query.get(NFT_id)
    print(nft)
    user_NFT = user_NFT_table.query.filter(user_NFT_table.NFT_id == NFT_id).first()
    data = {}
    print(nft, "       ",
          nft.NFT_id, "        ",
          nft.NFT_name, "       ",
          nft.img_url, "        ",
          nft.NFT_description, "        ",
          nft.NFT_time, "        ",
          )

    data['NFT_id'] = nft.NFT_id
    data['NFT_name'] = nft.NFT_name
    data['img_url'] = nft.img_url
    data['NFT_description'] = nft.NFT_description
    data['NFT_time'] = nft.NFT_time.strftime("%Y-%m-%d %H:%M:%S")
    data['address'] = nft.address

    return data


@app.route('/api/NFT_user', methods=['POST'])
def user_nft_information_get():
    # 3.3 用户个人的NFT列表
    # 用户个人所拥有的NFT列表
    r = request.get_data()
    print(r)
    dict = json.loads(r)  # 重新编码
    print(dict)

    user_id = dict['UserID']
    print(user_id)

    # u = User.query.filter(User.user_id == user_id).first_or_404()
    user_NFT = user_NFT_table.query.filter(user_NFT_table.user_id == user_id).all()

    l = len(user_NFT)

    print(l)

    Data = {

    }
    i = 0

    for nft in user_NFT:
        NFT_item = NFT.query.filter(NFT.NFT_id == nft.NFT_id).first()
        print(NFT_item)
        data = {}
        data['NFT_owner']=NFT_item.owner
        data['NFT_id'] = NFT_item.NFT_id
        data['NFT_name'] = NFT_item.NFT_name
        data['img_url'] = NFT_item.img_url
        data['NFT_time'] = NFT_item.NFT_time
        data['address'] = NFT_item.address

        Data[str(i)] = data
        i = i + 1
    print(Data)
    return Data


# 上传照片生成NFT
@app.route('/api/upload_NFT', methods=['POST'])
def upload_NFT():
    print(request.files['file'])

    filename = request.files['file'].filename
    file = request.files['file']

    location = 'NFT/Image/'
    print("location = ", location)
    filename_url = files.save(file, location)
    print("filename = ", filename_url)
    url = files.url(filename_url)

    NFT_item = NFT(
        img_url=url,
        NFT_time=datetime.datetime.now(),
        creator = "棒棒糖home"
    )
    db.session.add(NFT_item)
    db.session.flush()
    print(NFT_item.NFT_id)
    icon = NFT_item.NFT_id

    # 实例化QRCode生成qr对象
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=4,
        border=2
    )
    # 传入数据 分辨率=（21+（version-1）*4+border*2）*box_size

    img = qrcode.make(icon)
    QRcode_name = filename
    print('QRcode_name', QRcode_name)
    img.save("./flaskr/static/NFT/QRcode/" + QRcode_name)
    # basedir = os.path.abspath(os.path.dirname("./flaskr/static/NFT/QRcode/"+QRcode_name))
    QRcode_url = 'http://127.0.0.1:5000/_uploads/files/NFT/QRcode/' + QRcode_name
    #QRcode_url = 'https://bangbangtang.club/_uploads/files/NFT/QRcode/' + QRcode_name
    print(QRcode_url)
    NFT_item.QRcode_url = QRcode_url
    db.session.commit()
    # 展示二维码

    return QRcode_url


# 扫描二维码获取NFT
@app.route('/api/Get_NFT', methods=['POST'])
def Get_NFT():
    r = json.loads(request.get_data())
    print(r,'173')
    user_id = r['UserID']
    user=User.query.filter(User.user_id==user_id).first()
    NFT_id = r['NFT_ID']
    NFT_item = NFT.query.filter(NFT.NFT_id == NFT_id).first()
    print(NFT_item)
    NFT_Bool = user_NFT_table.query.filter(and_(user_NFT_table.NFT_id == NFT_id, user_NFT_table.user_id == user_id)).first()
    print(NFT_Bool)
    data = {}
    if (NFT_Bool):
        data['NFT_name'] =NFT_item.NFT_name
        data['exist'] = 1
        data['img_url'] = NFT_item.img_url
        print('exist')
        return data


    else:

        ri = NFT_item.img_url.rindex('/')
        NFT_name = NFT_item.img_url[ri + 1:]
        all_the_text = open('/Users/huangzexi/PycharmProjects/end_demo11.28/flaskr/static/NFT/QRcode/' + NFT_name,'rb').read()
        #all_the_text = open('/root/myflask/flaskr/static/NFT/QRcode/' + NFT_name,'rb').read()
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
        db.session.add(uer_nft_item)
        db.session.flush()
        db.session.commit()

        data['exist'] = 0
        data['img_url'] = NFT_item.img_url

        NFT_item.owner=user.name
        NFT_item.address=NFT_test['address']
        NFT_item.transection_time=NFT_item.NFT_time
        db.session.flush()
        db.session.commit()
        print(data)
        return data


# 修改NFT名称
@app.route('/api/NFT_Name', methods=['POST'])
def NFT_Name():
    r = json.loads(request.get_data())
    print(r)
    nft_item = NFT.query.filter(NFT.NFT_id==r['NFT_id']).first()
    nft_item.NFT_name=r['NFT_name']
    db.session.commit()
    nft_user_item= user_NFT_table.query.filter(NFT.NFT_id==r['NFT_id']).first()
    nft_user_item.NFT_name = r['NFT_name']
    db.session.commit()
    print('nft_user_item',nft_user_item,'nft_item',nft_item)

    return '1'

# NFT验证
@app.route('/api/NFT_Verify', methods=['POST'])
def NFT_verify():
    r = json.loads(request.get_data())
    print(r)
    data={}
    #user_nft_item=user_NFT_table.query.filter(user_NFT_table.signature==r['signature']).first()
    NFT_item=NFT.query.filter(NFT.address==r['address']).first()
    print(NFT_item)

    data['NFT_url']=NFT_item.img_url
    data['NFT_address']=NFT_item.address
    data['NFT_name'] = NFT_item.NFT_name
    data['owner']=NFT_item.owner
    data['creator']=NFT_item.creator
    data['create_time']=NFT_item.NFT_time.strftime("%Y-%m-%d %H:%M:%S")
    data['transection_time']=NFT_item.transection_time.strftime("%Y-%m-%d %H:%M:%S")
    return data