var app = getApp()
Page({
  data: {
    userInfo: {},
    hasUserInfo: false,
    canIUseGetUserProfile: false,
  },
  wx_login(e){
    wx.switchTab({
      url: '/pages/index/index',
    })
  },
  getUserProfile(e) {
    
    // 已经授权，可以直接调用 getUserInfo 获取头像昵称，不会弹框
    wx.getUserProfile({
      lang: 'zh_CN',
      desc: '完善资料',
      success: userResult => {
        this.setData({
          userInfo: userResult.userInfo
        })
       //设置本地缓存
        console.log(this.data.userInfo)
        console.log(userResult)
        wx.login({
          success: resp => {
            // 发送 res.code 到后台换取 openId, sessionKey, unionId
            console.log(resp);
            console.log(resp.code)
            var that = this;
            // 获取用户信息
            var platUserInfoMap = {}
            platUserInfoMap["encryptedData"] = userResult.encryptedData;
            platUserInfoMap["iv"] = userResult.iv;
            wx.request({
              url: app.globalData.Url+'/register',
              data: {
                platCode: resp.code,
                platUserInfoMap: platUserInfoMap,
                userInfo: userResult.userInfo
              },
              header: {
                "Content-Type": "application/json"
              },
              method: 'POST',
              dataType: 'json',
              success: (res) => {
                console.log(res)
                app.globalData.name = res.data.openid
                console.log(app.globalData.name)
                wx.setStorageSync(
                  "userinfo", {
                    avatarUrl: userResult.userInfo.avatarUrl,
                    name: userResult.userInfo.nickName,
                    gender: userResult.userInfo.gender,
                    province: userResult.userInfo.province,
                    openid:res.data.openid,
                    userid:res.data.userid
                  }
                ) 
                wx.getStorage({
                  key: 'userinfo',
                  success(res) {
                    console.log(res)
                    wx.switchTab({
                      url: '/pages/index/index',
                    })
                  }
                })
              },

              fail: function (err) {}, //请求失败
              complete: function () {} //请求完成后执行的函数
            })
          }
        })
      }
    })
  },
  
})