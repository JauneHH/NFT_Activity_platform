// pages/movie/movie.js
var app=getApp()
Page({
  /**
   * 页面的初始数据
   * {
        name: '活动A',
        time: '2021-07-14',
        area: '上海市',
        status: '已参与'
      }, {
        name: '活动B',
        time: '2021-07-29',
        area: '杭州市',
        status: '已参与'
      }, {
        name: '活动C',
        time: '2021-07-23',
        area: '杭州市',
        status: '未参与'
      },
      {
        name: '路演',
        time: '2021-07-31',
        area: '上海市',
        status: '未参与'
      }
   */
  data: {
    curNav: '全部',
    activity: [
    ],
    status_item: [{
      name: '全部',
      id:'2'
    }, {
      name: '已参与',
      id:'1'
    }, {
      name: '未参与',
      id:'0'
    }]
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.setData({
      curNav: options.data
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
    wx.getStorage({
      key: 'userinfo',
      success:(res) =>{
        console.log(res)
        wx.request({

          url: app.globalData.Url+'/api/activity_user',
          data: {
            open_id: res.data.openid
          },
          header: {
            "Content-Type": "application/json"
          },
          method: 'POST',
          dataType: 'json',
          success: (res) => {
            console.log(res.data)
            this.setData({
              activity: res.data
            })
            console.log(this.data.activity)
          },
        })

      }
    })
 
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

  change_status(e) {
    var id = e.currentTarget.dataset.id;
    this.setData({
      curNav: id
    })
    console.log(this.data.curNav)
  },

  activityInformationStatus: function (e) {
    console.log(e.currentTarget.id)
   
    console.log(this.data.activity)
    for (var i in this.data.activity) 
    {
      if(e.currentTarget.id==this.data.activity[i].id){
        console.log(this.data.activity[i])
        var activity_item=this.data.activity[i]
        wx.navigateTo({
          url: '/pages/activity/activity_upload/activity_upload?name='+activity_item.name+'&area=' + activity_item.area+'&type=' + activity_item.activity_celebrity+'&time='+activity_item.time+'&id='+activity_item.id+'&img_url='+activity_item.img_url
        })
      }
    }
  },

  
})