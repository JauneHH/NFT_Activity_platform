var app = getApp()   
Page({
  data: {
        p:'',
        s:'',
        r:'',
        c:'',
  },
  onLoad: function (options) {

    console.log("程序启动")
  },
  scanCodeClick: function () {
    onlyFromCamera: true,
    wx.scanCode({
      //success使用箭头函数
      success:(res)=>{
        var _this = this;
        console.log(res.result);
        _this.setData({r:res.result});
        console.log(res.scanType);
        _this.setData({s:res.scanType});
        console.log(res.charSet);
        _this.setData({c:res.charSet});
        console.log(res.path);
        _this.setData({p:res.path});
      },
      fail: function (res) {},
      complete: function (res) {
      }
    })
  },
})
