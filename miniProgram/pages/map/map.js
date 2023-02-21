// pages/map/map.js
var QQMapWX = require('/qqmap-wx-jssdk.js');
var qqmapsdk;
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
    qqmapsdk = new QQMapWX({
      key: 'SMEBZ-D3RW4-OMNUP-XK2VR-7LQJH-DXFB6' //这里自己的secret秘钥进行填充
    });
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
  huoQu: function(e) {
    wx.getLocation({
      success: function (res) {
        console.log(res);
      },
    })
},
chaKan: function (e) {
  wx.getLocation({
    success: function (res) {
      console.log(res);
      wx.openLocation({
        latitude: res.latitude,
        longitude: res.longitude,
        
      })
    },
  })

},
xuanZe: function (e) {
  wx.chooseLocation({
    success: function (res) {
      console.log(res);
    }
  })
},
autoGetLocation:function(e) {
  qqmapsdk.geocoder({
    //获取表单传入地址
    address: '上海市杨浦区淞沪路2005号', //地址参数，例：固定地址，address: '北京市海淀区彩和坊路海淀西大街74号'
    success: function(res) {//成功后的回调
      console.log(res);
      var res = res.result;
      var latitude = res.location.lat;
      var longitude = res.location.lng;
      //根据地址解析在地图上标记解析地址位置
      wx.openLocation({
        latitude: res.location.lat,
        longitude: res.location.lng,
        
      })
    },
    fail: function(error) {
      console.error(error);
    },
    complete: function(res) {
      console.log(res);
    }
  })
}
})