// app.js
var QQMapWX = require('utils/qqmap-wx-jssdk.js');
var qqmapsdk;
App({
  onLoad: function (options) {
    
    qqmapsdk = new QQMapWX({
      key: 'SMEBZ-D3RW4-OMNUP-XK2VR-7LQJH-DXFB6' //这里自己的secret秘钥进行填充
    });
  },
  onLaunch() {
    // 展示本地存储能力

  },
  globalData: {
   
    Url: 'http://10.162.249.252:5000'
  }
})