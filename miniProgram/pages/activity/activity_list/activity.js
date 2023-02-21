var app=getApp()
Page({

    data: {
        curNav: 0,
        activity: '',
        Search_List: {},
        title: [{
            "id": 0,
            "name": "全部分类"
        }, ],
        goods: [

        ],
        container_is_show: true,
    },
    onLoad: function (options) {

    },

    /**
     * 生命周期函数--监听页面初次渲染完成
     */
    onReady: function () {
        wx.request({
            url: app.globalData.Url+'/api/activity_list',
            data: {},

            header: {
                "Content-Type": "application/json"
            },
            method: 'POST',
            dataType: 'json',

            success: (res) => {
                console.log(res.data),
                    this.setData({
                        activity: res.data,
                    })

                for (var item in res.data) {
                    let flag = 1;

                    for (var title_item in this.data.title) {
                        if (this.data.title[title_item]['name'] == res.data[item]['type']) {
                            flag = 0
                        }
                    }
                    if (flag != 0) {
                        if (res.data[item]['type']) {
                            let title_length = this.data.title.length
                            let newItem = {
                                'id': title_length,
                                'name': res.data[item]['type'],
                            }
                            this.data.title.push(newItem)
                            this.setData({
                                title: this.data.title
                            })
                        }
                    }
                    this.setData({
                        goods: res.data
                    })
                }
                console.log(this.data.title, this.data.List)

            },
            fail: function (err) {}, //请求失败
            complete: function () {} //请求完成后执行的函数
        })
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

    // 单击改变样式
    click: function (e) {
        var ids = e.currentTarget.dataset.id; //获取自定义的id 
        var id;
        console.log(ids)
        var good = "";
        if (ids == 0) {
            id = 0
            this.setData({
                curNav: id
            })

        } else {

            for (var item in this.data.title) {
                if (ids == this.data.title[item].id) {
                    id = ids;
                    this.setData({
                        curNav: this.data.title[item].name
                    })
                }
            }
        }
        console.log(this.data.curNav)
    },

    activity_information: function (e) {

        var that = this
        var activity_item = {}
        console.log(e.currentTarget.dataset.id)
        console.log(this.data.goods)
        for (var item in this.data.goods)

            if (e.currentTarget.dataset.id == this.data.goods[item].id) {
                activity_item = this.data.goods[item]
            }
        console.log(activity_item)
        wx.navigateTo({

            url: '/pages/activity/activity_information/activity_information?id=' + activity_item.id
        })
    },
    onSearch: function (e) {
        console.log(e)
        wx.request({
            url: app.globalData.Url+'/api/activity_search',
            data: {

                name: e.detail
            },

            header: {
                "Content-Type": "application/json"
            },
            method: 'POST',
            dataType: 'json',
            success: (res) => {
                console.log(res.data)
                this.setData({
                    Search_List: res.data
                })
            },

        })
        let flag = !this.data.container_is_show
        this.setData({
            container_is_show: flag
        })
    },
    onCancel: function (e) {
        let flag = !this.data.container_is_show
        this.setData({
            container_is_show: flag
        })
    }
})