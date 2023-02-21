// pages/user_information/activity_result/activity_result.js
var app =getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    
    activity_information:{},
    activity_name: null,
    activity_area: null,
    activity_type: null,
    activity_time: null,
    activity_id: null,
    activity_img_url: null,
    has_upload_imgs_type:[],
    activity_result:{},
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that =this
    console.log(options)
    this.setData({
      activity_id:options.activity_id
    })
    wx.request({

      url: app.globalData.Url + '/api/activity_result',
      data: {
        activity_id:options.activity_id
      },

      header: {
        "Content-Type": "application/json"
      },
      method: 'POST',
      dataType: 'json',
      success: (res) =>{
        console.log(res)
        this.setData({
          activity_result:res.data
        })
        
        for(var user_item in res.data){
            var type_list = []
            console.log(res.data[user_item].pictrue_list)
            var activity_result_item=that.data.activity_result
            for (var item in res.data[user_item].pictrue_list) {
              var media_item = res.data[user_item].pictrue_list[item]
              console.log(media_item)
              var index = media_item.lastIndexOf("."); //（考虑严谨用lastIndexOf(".")得到）得到"."在第几位
              var img_id = media_item.substring(index); //截断"."之前的，得到后缀
              if (img_id != ".bmp" && img_id != ".png" && img_id != ".gif" && img_id != ".jpg" && img_id != ".jpeg") { //根据后缀，判断是否符合图片格式
                console.log("不是指定图片格式,重新选择");
                type_list.push({
                  'url': media_item,
                  'type': 'video'
                })

              } else {
                console.log("图片格式");
                type_list.push({ 
                  'url': media_item,
                  'type': 'image'
                })
              }
            }
            activity_result_item[user_item]['picture_list']=type_list
            console.log(activity_result_item[user_item])
            that.setData({
              activity_result:activity_result_item
            })
          }
          console.log(this.data.activity_result,'++',that.data.activity_result)
      },
    }),
    wx.request({

      url: app.globalData.Url + '/api/activity_information',
      data: {
        id:options.activity_id
      },

      header: {
        "Content-Type": "application/json"
      },
      method: 'POST',
      dataType: 'json',
      success: (res) =>{
        console.log(res)
        this.setData({
          activity_information:res.data
        })
      },
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
  previewImg: function (e) {
    var urls=[]
    //获取当前图片的下标
    console.log(e.currentTarget.dataset)
    var index = e.currentTarget.dataset.index;
    var current=e.currentTarget.dataset.picture_url
    //所有图片
    var imgs = this.data.activity_result[index].picture_list;
    var urls = []
    for (var i in imgs) {
      if (imgs[i].type == 'image') {
        urls.push(imgs[i].url)
      }

    }
   
    wx.previewImage({
      //当前显示图片
      current: current,
      //所有图片
      urls: urls
    })

  },
})