// pages/activity/activity_upload/activity_upload.js
import Dialog from '/../../../miniprogram_npm/@vant/weapp/dialog/dialog';
var app=getApp()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    qrCode_url:'',
    qrCode_list:[],
    has_upload: false,
    show: false,
    imgs: [],
    show_qrCode:false,
    has_upload_imgs:[],
    name: null,
    area: null,
    type: null,
    time: null,
    id: null,
    img_url: null,
    comment: null,
    user_activity_status:null,
    user_id:null,
  },


  onClose() {
    this.setData({
      show: false
    });
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    console.log(options)
    
    this.setData({
      id: options.id,
      name: options.name,
      area: options.area,
      type: options.type,
      time: options.time,
      img_url: options.img_url
    })
    console.log(this.data.user_id)
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
 
  //选择视频与图片
  chooseMedia: function (e) {
    var imgs = this.data.imgs
    var that = this
    wx.chooseMedia({
      count: 9,
      sizeType: ['original', 'compressed'],
      mediaType: ['image', 'video'],
      sourceType: ['album', 'camera'],
      maxDuration: 30,
      camera: 'back',
      success(res) {

        var media = res.tempFiles
        for (var i = 0; i < media.length; i++) {
          var mediaItem = {}
          mediaItem.tempFilePath = media[i].tempFilePath,
            mediaItem.type = res.type,
            imgs.push(mediaItem);
          console.log(res)
        }
        that.setData({
          imgs: imgs
        })
      }
    })
    console.log(this.data.imgs)
  },
  deleteImg: function (e) {
    var imgs = this.data.imgs;
    var index = e.currentTarget.dataset.index;
    imgs.splice(index, 1);
    this.setData({
      imgs: imgs
    });

  },
  //浏览待上传图片
  previewImg: function (e) {
    //获取当前图片的下标
    console.log(e.currentTarget.dataset)
    var index = e.currentTarget.dataset.index;
    //所有图片
    var imgs = this.data.imgs;
    var urls = []
    for (var i in imgs) {
      if (imgs[i].type == 'image') {
        urls.push(imgs[i].tempFilePath)
      }

    }
    console.log(urls)
    wx.previewImage({
      //当前显示图片
      current: imgs[0].tempFilePath,
      //所有图片
      urls: urls
    })
  },

   //浏览待上传图片
   previewQRCodeImg: function (e) {
    //获取当前图片的下标
    console.log(e)
    var QRList=[]
    QRList.push(e.currentTarget.dataset.src)
    wx.previewImage({
      //当前显示图片
      current: e.currentTarget.dataset.src,
      //所有图片
      urls: QRList
    })
  },
  //浏览图片
  previewUploadImg: function (e) {
    //获取当前图片的下标
    console.log(e.currentTarget.dataset)
    var index = e.currentTarget.dataset.index;
    //所有图片
    var imgs = this.data.has_upload_imgs;
    var urls = []
    for (var i in imgs) {
        urls.push(imgs[i])
    }
    console.log(urls)
    wx.previewImage({
      //当前显示图片
      current: imgs[0],
      //所有图片
      urls: urls
    })

  },
  //浏览多媒体资源
  previewMed: function (e) {
    var imgs = this.data.imgs;
    var sources = []
    for (var i in imgs) {
      var img = []
      img.url = imgs[i].tempFilePath
      img.type = imgs[i].type
      if (imgs[i].type == 'video') {
        sources.push(img)
      }
    }
    wx.previewMedia({
      sources: sources,
      success: (result) => {
        console.log(result)
      },
      fail: (result) => {
        console.log(result)
      }
    })
    console.log(sources)
  },
  //上传图片
  UploadMedia: function (event) {
    console.log(event)
    var imgs = this.data.imgs;
    Dialog.confirm({
        title: '上传图片/视频',
        message: '确认上传',
      })
      .then(() => {
        let flag = !this.data.has_upload
        this.setData({
          has_upload: flag
        })
        // on confirm
        for (var i = 0; i < imgs.length; i++) {
          console.log(i)
          var count = i + 1
          wx.showLoading({
            title: '正在上传第' + count + '张',
          })
          wx.uploadFile({
            url: app.globalData.Url+'/api/upload_NFT', // 仅为示例，非真实的接口地址
            filePath: imgs[i].tempFilePath,
            name: 'file',
            formData: {
              type: 'img'
            },
            header: {
              "Content-Type": "application/json"
            },
            method: 'POST',
            dataType: 'json',
            success: (res) => {
              console.log(res.data)
              this.setData({
                Search_List: res.data,
                
                qrCode_url:res.data,
              })
            },
            fail:(e)=>{
              console.log(e)
            }
          });
        }
        wx.showToast({
          title: '传输完成',
          duration: 1000,
          
          success:(e)=>{
            this.setData({
              show_qrCode:!this.data.show_qrCode
            })
          }
        })
        wx.hideLoading()
        // on cancel
      })
      .catch(() => {
        // 当设置 mutiple 为 true 时, file 为数组格式，否则为对象格式
        //跳转猫眼

      });
  },

})