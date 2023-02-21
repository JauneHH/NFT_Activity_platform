from flaskr import app
from flaskr.Models import models, middle
from flaskr.commands import command, command_test
from flaskr.views import activity, user, upload, NFT, backmanager,web_platform,test_lxr
from flask_cors import *

# from flaskr import app
# from flaskr.Models import models
# from flaskr.commands import command, command_test
# from flaskr.views import activity, user, upload, NFT, backmanager, ciyun_demo

CORS(app, supports_credentials=True)

@app.route('/')
def hello_a():
    return "Hello !"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
