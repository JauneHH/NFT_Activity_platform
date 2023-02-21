// pages/activity/activity_information/activity_information.js
var QQMapWX = require('/qqmap-wx-jssdk.js');
var qqmapsdk;
var app = getApp()
import Dialog from '/../../../miniprogram_npm/@vant/weapp/dialog/dialog';
Page({

  /**
   * 页面的初始数据
   */
  data: {
    market_list: {},
    button_style: 0,
    activity_information: '',
    name: null,
    area: null,
    type: null,
    time: null,
    id: null,
    img_url: null,
    description: null,
    show: false,
    market_show: false,
    user_number: null,
    img_list: ["http://127.0.0.1:5000/_uploads/files/video/img1.png",
      "http://127.0.0.1:5000/_uploads/files/video/img2.png",
      "http://127.0.0.1:5000/_uploads/files/video/img3.png"
    ]
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
  market_showPopup() {
    this.setData({
      market_show: true
    });
  },

  market_onClose() {
    this.setData({
      market_show: false
    });
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var user_id
    var that = this
    that.setData({
      id: options.id
    })
    console.log(options)


    qqmapsdk = new QQMapWX({
      key: 'SMEBZ-D3RW4-OMNUP-XK2VR-7LQJH-DXFB6' //这里自己的secret秘钥进行填充
    });
    var that = this;
    var id = that.data.id
    wx.getLocation({
        type: 'wgs84', //wgs84 返回 gps 坐标，gcj02 返回可用于 wx.openLocation 的坐标
        success(res) {
          const latitude = res.latitude
          const longitude = res.longitude
          const speed = res.speed
          const accuracy = res.accuracy
          console.log(res)
          qqmapsdk.reverseGeocoder({
            location: {
              latitude,
              longitude
            },
            success(res) {
              console.log('success', res.result.ad_info)
              wx.request({
                url: app.globalData.Url + '/api/activity_market',
                data: {
                  city: res.result.ad_info.city,
                  area: res.result.ad_info.district
                },
                header: {
                  "Content-Type": "application/json"
                },
                method: 'POST',
                dataType: 'json',
                success: (res) => {
                  console.log(res.data)
                  that.setData({
                    market_list: res.data
                  })

                },

              })
            }
          })
        }
      }),
      wx.getStorage({
        key: 'userinfo',
        success: (res) => {
          console.log(res)
          var user_id = res.data.userid
          wx.request({

            url: app.globalData.Url + '/api/activity_information',
            data: {
              id: id,
              user_id: user_id
            },
            header: {
              "Content-Type": "application/json"
            },
            method: 'POST',
            dataType: 'json',
            success: (res) => {
              console.log(res.data)
              this.setData({
                activity_information: res.data,
                id: res.data.id,
                name: res.data.name,
                area: res.data.area,
                type: res.data.type,
                time: res.data.time,
                img_url: res.data.img_url,
                description: res.data.description,
                user_number: res.data.users_number,
                button_style: res.data.user_has_attend
              })
              console.log(this.data.activity_information)
            },
          })
        },
        fail: (res) => {
          console.log(res)
          wx.request({

            url: app.globalData.Url + '/api/activity_information',
            data: {
              id: id,
            },
            header: {
              "Content-Type": "application/json"
            },
            method: 'POST',
            dataType: 'json',
            success: (res) => {
              console.log(res.data)
              this.setData({
                activity_information: res.data,
                id: res.data.id,
                name: res.data.name,
                area: res.data.area,
                type: res.data.type,
                time: res.data.time,
                img_url: res.data.img_url,
                description: res.data.description,
                user_number: res.data.users_number,
                button_style: res.data.user_has_attend
              })
              console.log(this.data.activity_information)
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
    console.log('button_style', this.data.button_style)
    var id = this.data.id
    wx.getStorage({
      key: 'userinfo',
      success: (res) => {
        console.log(res)
        var user_id = res.data.userid
        wx.request({

          url: app.globalData.Url + '/api/activity_information',
          data: {
            id: id,
            user_id: user_id
          },
          header: {
            "Content-Type": "application/json"
          },
          method: 'POST',
          dataType: 'json',
          success: (res) => {
            console.log(res.data)
            this.setData({
              activity_information: res.data,
              id: res.data.id,
              name: res.data.name,
              area: res.data.area,
              type: res.data.type,
              time: res.data.time,
              img_url: res.data.img_url,
              description: res.data.description,
              user_number: res.data.users_number,
              button_style: res.data.user_has_attend
            })
            console.log(this.data.activity_information)
          },
        })
      },
      fail: (res) => {
        console.log(res)
        wx.request({

          url: app.globalData.Url + '/api/activity_information',
          data: {
            id: id,
          },
          header: {
            "Content-Type": "application/json"
          },
          method: 'POST',
          dataType: 'json',
          success: (res) => {
            console.log(res.data)
            this.setData({
              activity_information: res.data,
              id: res.data.id,
              name: res.data.name,
              area: res.data.area,
              type: res.data.type,
              time: res.data.time,
              img_url: res.data.img_url,
              description: res.data.description,
              user_number: res.data.users_number,
              button_style: res.data.user_has_attend
            })
            console.log(this.data.activity_information)
          },
        })
      }
    })

    console.log(this.data.button_style)
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


  attendActivity: function () {
    var that = this
    var name = this.data.name
    var area = this.data.area
    var type = this.data.type
    var time = this.data.time
    var id = this.data.id
    var img_url = this.data.img_url
   
    wx.getStorage({
      key: 'userinfo',
      success: (res) => {
        console.log(res)
        Dialog.confirm({
            title: '参与活动',
            message: '确认参与',
          })
          .then(() => {
            wx.request({
              url: app.globalData.Url + '/api/activity_attend',
              data: {
                user_id: res.data.userid,
                activity_id: this.data.id
              },

              header: {
                "Content-Type": "application/json"
              },
              method: 'POST',
              dataType: 'json',
              success: function (res) {
                wx.showToast({
                  title: '已成功参与',
                  duration: 3000
                });
                console.log(res.data)


                wx.navigateTo({
                  url: '/pages/activity/activity_upload/activity_upload?name=' + name + '&area=' + area + '&type=' + type + '&time=' + time + '&id=' + id + '&img_url=' + img_url,
                })
              },
            })

            that.onShow()
          })
          .catch(() => {});
        this.setData({
          show: false
        });

      },
      fail: (res) => {
        console.log(res)
        wx.getUserProfile({
          lang: 'zh_CN',
          desc: '完善资料',
          success: userResult => {
            this.setData({
              userInfo: userResult.userInfo
            })
            //设置本地缓存
            console.log(this.data.userInfo)
            console.log(userResult)
            wx.login({
              success: resp => {
                // 发送 res.code 到后台换取 openId, sessionKey, unionId
                console.log(resp);
                console.log(resp.code)
                var that = this;
                // 获取用户信息
                var platUserInfoMap = {}
                platUserInfoMap["encryptedData"] = userResult.encryptedData;
                platUserInfoMap["iv"] = userResult.iv;
                wx.request({
                  url: app.globalData.Url + '/register',
                  data: {
                    platCode: resp.code,
                    platUserInfoMap: platUserInfoMap,
                    userInfo: userResult.userInfo
                  },
                  header: {
                    "Content-Type": "application/json"
                  },
                  method: 'POST',
                  dataType: 'json',
                  success: (res) => {
                    console.log(res)
                    app.globalData.name = res.data.openid
                    console.log(app.globalData.name)
                    wx.setStorageSync(
                      "userinfo", {
                        avatarUrl: userResult.userInfo.avatarUrl,
                        name: userResult.userInfo.nickName,
                        gender: userResult.userInfo.gender,
                        province: userResult.userInfo.province,
                        openid: res.data.openid,
                        userid: res.data.userid
                      }
                    )
                    wx.getStorage({
                      key: 'userinfo',
                      success(res) {
                        console.log(res)
                      }
                    })
                  },
                })
              }
            })
          }

        })
      }
    })


  },
  finishActivity:function(e){
    var that = this
    var name = this.data.name
    var area = this.data.area
    var type = this.data.type
    var time = this.data.time
    var id = this.data.id
    var img_url = this.data.img_url
    wx.navigateTo({
      url: '/pages/activity/activity_upload/activity_upload?name=' + name + '&area=' + area + '&type=' + type + '&time=' + time + '&id=' + id + '&img_url=' + img_url,
    })
  },

  autoGetLocation: function (e) {
    console.log(e.currentTarget.dataset.id),
      qqmapsdk.geocoder({
        //获取表单传入地址
        address: e.currentTarget.dataset.id,
        //address: '上海市杨浦区淞沪路2005号', 
        //地址参数，例：固定地址，address: '北京市海淀区彩和坊路海淀西大街74号'
        success: function (res) { //成功后的回调
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
        fail: function (error) {
          console.error(error);
        },
        complete: function (res) {
          console.log(res);
        }
      })
  },
  market_address: function (e) {
    console.log(e.currentTarget.dataset.id),
      qqmapsdk.geocoder({
        //获取表单传入地址
        address: e.currentTarget.dataset.id,
        //address: '上海市杨浦区淞沪路2005号', 
        //地址参数，例：固定地址，address: '北京市海淀区彩和坊路海淀西大街74号'
        success: function (res) { //成功后的回调
          console.log(res);
          var res = res.result;
          //根据地址解析在地图上标记解析地址位置
          wx.openLocation({
            latitude: res.location.lat,
            longitude: res.location.lng,

          })
        },
        fail: function (error) {
          console.error(error);
        },
        complete: function (res) {
          console.log(res);
        }
      })
  },
  previewImg: function (e) {
    //获取当前图片的下标
    console.log(e)

    wx.previewImage({
      //当前显示图片
      current: this.data.activity_information.activity_img_list[0],
      //所有图片
      urls: this.data.activity_information.activity_img_list
    })
  },

  activity_result(e) {
    wx.navigateTo({
      url: '/pages/activity/activity_result/activity_result?activity_id=' + this.data.id,
    })
  }
})