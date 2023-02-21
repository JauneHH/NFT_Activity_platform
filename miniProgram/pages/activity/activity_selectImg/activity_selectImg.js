// pages/activity/activity_selectImg/activity_selectImg.js
import Dialog from '/../../../miniprogram_npm/@vant/weapp/dialog/dialog';
Page({

  /**
   * 页面的初始数据
   */
  data: {
    imgs: [],
    name: null,
    area: null,
    type: null,
    time: null,
    id: null,
    img_url: null
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
  /* 选择图片
  chooseImg: function (e) {
    var that = this;
    var imgs = this.data.imgs;
    if (imgs.length >= 9) {
      this.setData({
        lenMore: 1
      });
      setTimeout(function () {
        that.setData({
          lenMore: 0
        });
      }, 2500);
      return false;
    }
    wx.chooseImage({
      // count: 1, // 默认9
      sizeType: ['original', 'compressed'], // 可以指定是原图还是压缩图，默认二者都有
      sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有
      success: function (res) {
        console.log(res)
        // 返回选定照片的本地文件路径列表，tempFilePath可以作为img标签的src属性显示图片
        var tempFilePaths = res.tempFilePaths;
        var imgs = that.data.imgs;
        // console.log(tempFilePaths + '----');
        for (var i = 0; i < tempFilePaths.length; i++) {
          if (imgs.length >= 9) {
            that.setData({
              imgs: imgs
            });
            return false;
          } else {
            imgs.push(tempFilePaths[i]);
          }
        }
        // console.log(imgs);
        that.setData({
          imgs: imgs
        });
      }
    });
    console.log(this.data.imgs)
  },
  */
  // 删除图片
  deleteImg: function (e) {
    var imgs = this.data.imgs;
    var index = e.currentTarget.dataset.index;
    imgs.splice(index, 1);
    this.setData({
      imgs: imgs
    });

  },
  //浏览图片
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
      title: '标题',
      message: '弹窗内容',
    })
    .then(() => {
      // on confirm
      //跳转猫眼
      wx.setClipboardData({
        data: 'X8FCVX8RRLVLQ',
        success(res) {
          wx.navigateToMiniProgram({
            appId: 'wxdbb4c5f1b8ee7da1',
            
          })
        }
      });
      
    })
    .catch(() => {
          // 当设置 mutiple 为 true 时, file 为数组格式，否则为对象格式
    for (var i = 0; i < imgs.length; i++) {
      console.log(i)
      var count = i + 1
      wx.showLoading({
        title: '正在上传第' + count + '张',
      })
      wx.uploadFile({
        url: 'http://1.116.113.201:5000/demo/upload', // 仅为示例，非真实的接口地址
        filePath: imgs[i].tempFilePath,
        name: 'file',
        formData: {
          type: imgs[i].type
        },
      });
    }
    wx.showToast({
      title: '传输完成',
      duration: 1000
    })
    wx.hideLoading()
     // on cancel
    });

  },

})