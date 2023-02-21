// pages/user_information/user_information.js
var app = getApp();
Page({
  /**
   * 页面的初始数据
   */
  data: {
    userInfo: {},
    userid: null
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {


  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    wx.getStorage({
      key: 'userid',
      success: res_userid => {
        wx.getStorage({
          key: 'userinfo',
          success: res_userinfo => {
            console.log(res_userinfo)
            this.setData({
              userInfo: res_userinfo.data
            })
          }
        })
        this.setData({
          userid: res_userid.data.userid
        })
      }
    })


    console.log(this.data.userInfo)
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  },

  click: function () {
    this.setData({
      name: this.name
    })
  },

  get_user_activity(e) {
    wx.navigateTo({
      url: '/pages/user_information/activity_user/activity_user?data=' + e.currentTarget.dataset.id
    })
  },
  get_user_NFT(e) {
    wx.navigateTo({
      url: '/pages/NFT/NFT_user/NFT_user'
    })
  },
  upload_NFT(e) {
    wx.navigateTo({
      url: '/pages/user_information/upload_NFT/upload_NFT'
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
              url: app.globalData.Url + '/register',
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
                    openid: res.data.openid,
                    userid: res.data.userid
                  },
                )
                wx.setStorageSync(
                  "userid", {
                    userid: res.data.userid
                  },
                )
                wx.getStorage({
                  key: 'userinfo',
                  success(res) {
                    console.log(res)
                  }
                })

                this.onShow()
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