var adds = {};
const app = getApp()
Page({
  data: {
    imgs: [],
    formdata: '',
    fileList: [],
  },
  formSubmit: function (e) {
    console.log(e)
    var id = e.target.id
    adds = e.detail.value;
    adds.program_id = app.jtappid
    adds.openid = app._openid
    adds.zx_info_id = this.data.zx_info_id
    this.upload()
  },
  // 上传图片
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
        var tempFiles = res.tempFiles;
        var imgs = that.data.imgs;
        var fileTest=that.data.fileList
        // console.log(tempFilePaths + '----');
        for (var i = 0; i < tempFilePaths.length; i++) {
          if (imgs.length >= 9) {
            that.setData({
              imgs: imgs
            });
            return false;
          } else {
            imgs.push(tempFilePaths[i]);
            fileTest.push(tempFilePaths[i])
            
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
  upload: function () {
    var that = this
    for (var i = 0; i < this.data.img_arr.length; i++) {
      wx.uploadFile({
        url: 'http://127.0.0.1:5000//demo/upload',
        filePath: that.data.img_arr[i],
        name: 'content',
        formData: adds,
        success: function (res) {
          console.log(res)
          if (res) {
            wx.showToast({
              title: '已提交发布！',
              duration: 3000
            });
          }
        }
      })
    }
    this.setData({
      formdata: ''
    })
  },

  upimg: function () {
    var that = this;
    if (this.data.img_arr.length < 3) {
      wx.chooseImage({
        sizeType: ['original', 'compressed'],
        success: function (res) {
          that.setData({
            img_arr: that.data.img_arr.concat(res.tempFilePaths)
          })
        }
      })
    } else {
      wx.showToast({
        title: '最多上传三张图片',
        icon: 'loading',
        duration: 3000
      });
    }
  },

  afterRead:function(event) {
    var fileTest = this.data.fileList;
    console.log(event)
    const {file} = event.detail
    var imgs = this.data.imgs;
    // 当设置 mutiple 为 true 时, file 为数组格式，否则为对象格式
    for (var i = 0; i < imgs.length; i++)
    {
    wx.uploadFile({
      url: 'http://127.0.0.1:5000//demo/upload', // 仅为示例，非真实的接口地址
      filePath: imgs[i],
      name: 'file',
      formData: {
        user: 'test'
      },
      /*success(res) {
        fileTest.push(file);
        console.log(fileTest)
        // 上传完成需要更新 fileList
       
      },*/
    });
    
  }
    console.log(this.data.fileList)
  },
})