from flaskr.commands.command_test import forge1, forge2, forge3, forge4, forge5

"""
# 需要在服务器上直接运行， 得放在flaskr 平级
# pycharm 里面可以是因为执行命令为 
# /Users/log1c/.conda/envs/hello/bin/python /Users/log1c/Code/python/end_demo1/forge.py
"""


def forge():
    forge1()
    forge2()
    forge3()
    forge4()
    forge5()


if __name__ == '__main__':
    forge()
