var app = getApp()
Page({
      data: {
        value: '',
        userInfo: {},
        NFT_img_url: '',
        NFT_name: '',
        NFT_exist: '',
        NFT_id: '',
        hasUserInfo: false,
        canIUseGetUserProfile: false,
        show: false,
        imgs: ["https://bangbangtang.club/_uploads/files/video/img1.png",
          "https://bangbangtang.club//_uploads/files/video/img2.jpg",
          "https://bangbangtang.club//_uploads/files/video/img3.png"
        ],
      },
      onLoad() {
        if (wx.getUserProfile) {
          this.setData({
            canIUseGetUserProfile: true
          })
        }
      },

  scanCodeClick: function () {
        onlyFromCamera: true,
        wx.getStorage({
          key: 'userinfo',
          success: (resStorage) => {
            console.log(resStorage)
            wx.scanCode({
              //success使用箭头函数
              success: (res) => {
                var _this = this;
                var NFT_item = res.result
                console.log(res.result);

                _this.setData({
                  NFT_id: res.result
                });
                wx.request({
                  url: app.globalData.Url + '/api/Get_NFT',
                  data: {
                    UserID: resStorage.data.userid,
                    NFT_ID: NFT_item,
                  },
                  header: {
                    "Content-Type": "application/json"
                  },
                  method: 'POST',
                  dataType: 'json',
                  success: function (resRequest) {
                    console.log(resRequest)
                    _this.setData({
                      NFT_img_url: resRequest.data['img_url'],
                      NFT_exist: resRequest.data['exist'],
                      NFT_name: resRequest.data['NFT_name']
                    })
                  },
                })
                this.setData({
                  show: !this.data.show
                })
              }
            })

          },      
            fail:(res)=>{
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
                        url: app.globalData.Url+'/register',
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
                              openid:res.data.openid,
                              userid:res.data.userid
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
  getUserInfo(event) {
    console.log(event.detail);
  },

  onClose() {
    this.setData({
      show: false
    });
  },
  onChange(event) {
    var that = this
    console.log(event.detail);
    that.setData({
      NFT_name: event.detail
    })
  },
  NFT_name(event) {

    console.log(event.detail);
    wx.getStorage({
      key: 'userinfo',
      success: (res) => {
        console.log(res)
        wx.request({

          url: app.globalData.Url + '/api/NFT_Name',
          data: {
            UserID: res.data.userid,
            NFT_name: this.data.NFT_name,
            NFT_id: this.data.NFT_id
          },

          header: {
            "Content-Type": "application/json"
          },
          method: 'POST',
          dataType: 'json',
          success: function (res) {
            console.log(res)

          },
        })
      }
    })
  }
})