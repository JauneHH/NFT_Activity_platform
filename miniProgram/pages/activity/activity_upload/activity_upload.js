// pages/activity/activity_upload/activity_upload.js
const regeneratorRuntime = require('../../../lib/runtime/runtime')
var app = getApp()
const upload = (filePath, type, activity_id, user_id,count) => {
  return new Promise((resolve, reject) => {
    const uploadTask=wx.uploadFile({
      url: app.globalData.Url + '/api/activity_finished', // 仅为示例，非真实的接口地址
      filePath: filePath,
      type: type,
      name: 'file',
      formData: {
        type: type,
        activity_id: activity_id,
        user_id: user_id
      },
      header: {
        "Content-Type": "application/json"
      },
      method: 'POST',
      dataType: 'json',

      success: (res) => {
        console.log(res)
        resolve(res)
      },
    });
    count=count+1
    uploadTask.onProgressUpdate((res) => { 
     
      wx.showLoading({
        title: '上传第' + count+'个资源'+'('+res.progress+'%)'
      });
    })
   
  })
}
import Dialog from '/../../../miniprogram_npm/@vant/weapp/dialog/dialog';
Page({

  /**
   * 页面的初始数据
   */
  data: {
    has_upload: false,
    show: false,
    name: null,
    area: null,
    type: null,
    time: null,
    id: null,
    img_url: null,
    comment: null,
    user_activity_status: null,
    user_id: null,
    progress_percent: 0,
    progress_show: false,
    imgs: [],
    video: [],
    has_upload_imgs: [],
    has_upload_imgs_type: [],
    media_account: 0,
  },
  showPopup() {
    this.setData({
      show: true
    });
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
    var that = this
    wx.getStorage({
      key: 'userinfo',
      success: (res) => {
        console.log(res)
        this.setData({
          user_id: res.data.userid
        })
        wx.request({
          url: app.globalData.Url + '/api/user/activity_user_imgs',
          header: {
            "Content-Type": "application/json"
          },
          data: {
            user_id: res.data.userid,
            activity_id: this.data.id,
          },
          method: 'Post',
          dataType: 'json',
          success: (res) => {
            console.log(res.data)
            that.setData({
              has_upload_imgs: res.data['img_list'],
              comment: res.data['comment'],
              user_activity_status: res.data['user_activity_status'],
            })

            var type_list = []
            for (var item in that.data.has_upload_imgs) {
              var media_item = that.data.has_upload_imgs[item]
              console.log(that.data.has_upload_imgs[item])
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
            that.setData({
              has_upload_imgs_type: type_list
            })
            console.log(that.data.has_upload_imgs, that.data.has_upload_imgs_type)

          },
          fail: (res) => {
            console.log(res)
          }
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
  imgSubmit: function (e) {
    wx.navigateTo({
      url: '/pages/activity/activity_selectImg/activity_selectImg?name=' + this.data.name + '&area=' + this.data.area + '&type=' + this.data.type + '&time=' + this.data.time + '&id=' + this.data.id + '&img_url=' + this.data.img_url
    })
  },
  //选择视频与图片
  chooseMedia: function (e) {
    var imgs = this.data.imgs
    var that = this
    wx.chooseMedia({
      count: 9,
      sizeType: 'original',
      mediaType: ['image', 'video'],
      sourceType: ['album', 'camera'],
      maxDuration: 30,
      camera: 'back',
      compressed: 'false',
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
  chooseVideo: function (e) {
    var imgs = this.data.imgs
    var that = this
    wx.showLoading({
      title: '选取中'
    });
    wx.chooseVideo({
      camera: 'back',
      sourceType: ['album', 'camera'],
      compressed: false,
      maxDuration: 60,

      success: (result) => {
        console.log(result)
        var mediaItem = {}
        mediaItem.tempFilePath = result.tempFilePath,
          mediaItem.type = 'video',
          imgs.push(mediaItem);
        that.setData({
          imgs: imgs
        })
        wx.hideLoading(),
          wx.showToast({
            title: '选取成功',
            icon: 'success',
            duration: 3000
          })
      },
      fail: (res) => {
        wx.hideLoading(),
          wx.showToast({
            title: '选取失败',
            
            duration: 3000
          })
      },
      complete: (res) => {
        wx.hideLoading()
      },
    })
  },
  chooseImg: function (e) {
    var imgs = this.data.imgs
    var that = this
    wx.chooseImage({
      count: 9, // 最多可以选择的图片张数，默认9
      sizeType: ['original', 'compressed'], // original 原图，compressed 压缩图，默认二者都有
      sourceType: ['album', 'camera'], // album 从相册选图，camera 使用相机，默认二者都有
      success: (res) => {
        console.log(res)
        var images = res.tempFilePaths
        for (var i = 0; i < images.length; i++) {
          var imgItem = {}
          imgItem.tempFilePath = images[i],
            imgItem.type = 'image',
            imgs.push(imgItem);
        }
        that.setData({
          imgs: imgs
        })
      },
      fail: function () {
        // fail
      },
      complete: () => {
        console.log('imgs', this.data.imgs)
      }
    })
  },
  deleteImg: function (e) {
    var imgs = this.data.imgs;
    var index = e.currentTarget.dataset.index;
    console.log(e)
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
      current: imgs[index].tempFilePath,
      //所有图片
      urls: urls
    })

  },
  //浏览图片
  previewUploadImg: function (e) {
    //获取当前图片的下标
    console.log(e.currentTarget.dataset)
    var index = e.currentTarget.dataset.index;
    //所有图片
    var imgs = this.data.has_upload_imgs_type;
    var urls = []
    for (var i in imgs) {
      if (imgs[i].type == 'image') {
        urls.push(imgs[i].url)
      }
    }
    console.log(urls)
    wx.previewImage({
      //当前显示图片
      current: imgs[index].url,
      //所有图片
      urls: urls
    })

  },
  //浏览多媒体资源
  //封装上传文件

  //上传图片
  async init(event) {
    var imgs = this.data.imgs;
    console.log(imgs.length)
    console.log(event)
    
    for (var i = 0; i < imgs.length; i++) {

      console.log(i)
      var account = i + 1
      var flag_upload = false

      this.setData({
        media_account: i
      })
      var upload_media = upload(imgs[i].tempFilePath, imgs[i].type, this.data.id, this.data.user_id,i)
      
      await upload_media
      
    }
    wx.hideLoading()
    wx.showToast({
      title: '上传成功',
      icon: 'success',
      duration: 3000
    })
   

  },
  UploadMedia: function (event) {
    console.log(event)
    var imgs = this.data.imgs;
    Dialog.confirm({
        title: '上传图片/视频',
        message: '确认上传',
      })
      .then(() => {
        wx.request({
          url: app.globalData.Url + '/api/activity_finished_comment',
          data: {
            user_id: this.data.user_id,
            activity_id: this.data.id,
            comment: this.data.comment,
          },
          header: {
            "Content-Type": "application/json"
          },
          method: 'POST',
          dataType: 'json',
          success: (res) => {
            console.log(res.data)
          },
        })

        var that = this
        let flag = !this.data.has_upload
        this.setData({
          has_upload: flag
        })
        // on confirm 
        console.log(imgs.length)
        this.init()
        
        this.onShow()
        // on cancel
      })
      .catch(() => {
        //当设置 mutiple 为 true 时, file 为数组格式，否则为对象格式
        //跳转猫眼
      });
  },

  UploadComment: function (e) {
    this.setData({
      comment: e.detail
    })
  },

})