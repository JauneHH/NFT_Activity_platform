"""
通过评论，生成词云
# B站专栏：同济子豪兄 2019-5-23
"""

# 导入词云制作库wordcloud和中文分词库jieba
import jieba
import wordcloud


# 构建并配置词云对象w
w = wordcloud.WordCloud(width=1000,
                        height=700,
                        background_color='white',
                        font_path='../static/MSYH.TTC',
                        stopwords={'的','和'}
                        )
# 对来自外部文件的文本进行中文分词，得到string
import os
print(os.getcwd())
with open('../static/新时代中国特色社会主义.txt',encoding='utf-8') as f:
    txt = f.read()
    print(type(txt))



txtlist = jieba.lcut(txt)
string = " ".join(txtlist)

# 将string变量传入w的generate()方法，给词云输入文字
w.generate(string)

# 将词云图片导出到当前文件夹
w.to_file('../static/output5-village.png')
print("ojbk")
