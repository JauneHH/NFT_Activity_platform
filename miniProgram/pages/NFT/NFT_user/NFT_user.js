// pages/NFT/NFT_user/NFT_user.js
var app=getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    userInfo: {},
    NFT_list: [],
    NFT_count: '',
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this;

    wx.getStorage({
      key: 'userinfo',
      success: (res) => {
        console.log(res)
        that.setData({
          userInfo: res.data
        })
      }
    })
    wx.getStorage({
      key: 'userinfo',
      success: (res) => {
        console.log(res)
        wx.request({

          url: app.globalData.Url+'/api/NFT_user',
          data: {
            UserID: res.data.userid,

          },

          header: {
            "Content-Type": "application/json"
          },
          method: 'POST',
          dataType: 'json',
          success: function (res) {
            console.log(res)
            that.setData({
              NFT_list: res.data
            })
            console.log(that.data.NFT_list)
            var count = 0;
            for (var key in that.data.NFT_list) {
              count++;
            }
            that.setData({
              NFT_count: count
            })
            console.log(that.data)
          },
        })
      }
    })
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
  get_NFT_information(e) {
    console.log(e)
    wx.navigateTo({
      url: '/pages/NFT/NFT_information/NFT?id=' + e.currentTarget.dataset.id
      
    })
  }
})