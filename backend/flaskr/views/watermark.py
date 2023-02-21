#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/2/18 18:05
# @Author  : Log1c
# @File    : watermark.py
# @Software: PyCharm

# 导入包
from PIL import Image, ImageDraw, ImageFont
from flaskr.Models.models import User


def addWaterMark(location, name):
    # 图片路径
    imagefile = location
    text = "棒棒糖home\n" + name
    # 打开图片
    imageInfo = Image.open(imagefile)
    print(imageInfo.size)
    a,b=imageInfo.size
    font_size=int(a/30)
    # 获取图片尺寸
    # print(imageInfo.size)
    # 设置图片水印的字体的字号

    #font = ImageFont.truetype("/Users/huangzexi/PycharmProjects/end_demo11.28/flaskr/static/fonts/MSYH.TTC", font_size)
    font = ImageFont.truetype("/root/myflask/flaskr/static/fonts/MSYH.TTC", font_size)
    #font = ImageFont.truetype("/Users/log1c/Code/python/end_demo1/flaskr/static/fonts/MSYH.TTC", 36)

    # 创建Draw对象，用于之后绘制文字
    draw = ImageDraw.Draw(imageInfo)
    # 设置水印文字的位置（x,y)，文本，颜色，字体字号
    text_size_x, text_size_y = draw.textsize(text, font=font)
    text_xy = (imageInfo.size[0] - text_size_x, imageInfo.size[1] - 2 * text_size_y)
    draw.text(text_xy, text, fill=(20, 150, 200, 80), font=font)
    # 图片预览
    # imageInfo.show()
    # 图片保存
    imageInfo.save(location)


# def watermark(location, name):
#     image = Image.open(location)
#     # 打开要加水印的图片
#     text = "棒棒糖home\n" + name
#     # 提示要打水印的文字
#     font = ImageFont.truetype("/Users/log1c/Code/python/end_demo1/flaskr/static/fonts/MSYH.TTC", 20)
#     # 获得一个字体，你也可以自己下载相应字体，第二个值是字体大小
#     layer = image.convert('RGBA')
#     # 将图片转换为RGBA图片
#     text_overlay = Image.new('RGBA', layer.size)
#     # 依照目标图片大小生成一张新的图片 参数[模式,尺寸,颜色(默认为0)]
#     image_draw = ImageDraw.Draw(text_overlay)
#     # 画图
#     text_size_x, text_size_y = image_draw.textsize(text, font=font)
#     # 获得字体大小,textsize(text, font=None)
#     text_xy = (layer.size[0] - text_size_x, layer.size[1] - text_size_y)
#     # 设置文本位置 此处是右下角显示
#     image_draw.text(text_xy, text, font=font, fill=(0, 0, 0, 100))
#     # 设置文字，位置,字体,颜色和透明度
#     marked_img = Image.alpha_composite(layer, text_overlay)
#     # 将水印打到原图片上生成新的图片
#     marked_img.save('123Test.png')
#     print("已经生成图片")
#     # 保存图片
#     # marked_img.show()
#     # 显示图片（ 这里是生成一个临时文件，必须关闭图片 这段py代码才算结束 )


if __name__ == '__main__':
    # test
    addWaterMark("/Users/log1c/Code/python/end_demo1/flaskr/views/123.jpg", "gcf")

    # addWaterMark("/Users/log1c/Code/python/end_demo1/flaskr/views/origin_202111240950371292.jpg", "gcf")
