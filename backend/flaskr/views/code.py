import qrcode
data = 'http://www.baidu.com/'
img_file = r'./flaskr.png'
# 实例化QRCode生成qr对象
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=2,
    border=2
)
# 传入数据 分辨率=（29+（version-1）*4+border*2）*box_size
qr.add_data(data)

qr.make(fit=True)

# 生成二维码
img = qr.make_image()

# 保存二维码
img.save(img_file)
# 展示二维码
img.show()