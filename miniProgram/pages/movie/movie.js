// pages/movie/movie.js
Page({
  /**
   * 页面的初始数据
   */
  data: {

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

  send_message(e) {
    wx.getStorage({
      key: 'userinfo',
      success(res) {
        var cpid = Math.ceil(Math.random() * 2000);
        wx.request({
          url: 'http://logic.cn.utools.club/demo1',
          data: {
            open_id: res.data.openid,
            name: res.data.name,
            coupon_id: cpid
          },
          header: {
            "Content-Type": "application/json"
          },
          method: 'POST',
          dataType: 'json'
        })
        console.log('发送数据', res)
      }
    })
  }
})