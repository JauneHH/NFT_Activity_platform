"""
通过评论，生成词云
"""
import jieba
import wordcloud
# 导入词云制作库wordcloud和中文分词库jieba
from flaskr import app
from flaskr.Models.middle import user_activity_class

@app.route('/api/ciyun', methods=['GET'])
def get_ciyun():
    """
    生成词云
    """
    u_a_class = user_activity_class.query.all()
    # print(u_a_class)
    print(type(u_a_class))
    print(len(u_a_class))
    str = ""
    for ua in u_a_class:
        s = ua.comment
        str = str + s + '。'
        print(s)
    print(str)

    import os
    print(os.getcwd())

    # 构建并配置词云对象w
    w = wordcloud.WordCloud(width=1000,
                            height=700,
                            background_color='white',
                            font_path="flaskr/static/MSYH.TTC",
                            stopwords={'的', '和'}
                            )
    # 对来自外部文件的文本进行中文分词，得到string
    txtlist = jieba.lcut(str)
    string = " ".join(txtlist)


    # 将string变量传入w的generate()方法，给词云输入文字
    w.generate(string)

    # 将词云图片导出到当前文件夹
    w.to_file('flaskr/static/pinglun.png')
    print("ojbk")
    url = "http://127.0.0.1:5000/_uploads/files/pinglun.png"
    print("http://127.0.0.1:5000/_uploads/files/pinglun.png")
    return str





