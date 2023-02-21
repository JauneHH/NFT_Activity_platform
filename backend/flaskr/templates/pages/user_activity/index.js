var app = new Vue({
    el: "#app",
    data: {
        mp3arr : ["https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg", "https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg", "https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg"],

        url: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
        srcList: [
            'https://fuss10.elemecdn.com/8/27/f01c15bb73e1ef3793e64e6b7bbccjpeg.jpeg',
            'https://fuss10.elemecdn.com/1/8e/aeffeb4de74e2fde4bd74fc7b4486jpeg.jpeg'
        ],
        user_upload_img:[],
        form: {

            url_list: ["../../img/bg1.jpg", "../../img/head.jpg", "../../img/bg2.jpg"],
            url_list_select: [],
        },
        activity_id:'',
        tableUser:[
        ],
    },
    download(name, href) {
        var a = document.createElement("a"), //创建a标签
            e = document.createEvent("MouseEvents"); //创建鼠标事件对象
        e.initEvent("click", false, false); //初始化事件对象
        a.href = href; //设置下载地址
        a.download = name; //设置下载文件名
        a.dispatchEvent(e); //给指定的元素，执行事件click事件
    },
    mounted(){
        this.activity_user_list()
    },
    methods: {
        cellStyle({row, column, rowIndex, columnIndex}) {
            if (row.user_activity_status == "待上传结果") {
                if (columnIndex == 4) {

                    return 'font-weight:bold;color:#909399'
                }
            } else  if (row.user_activity_status == "待审核") {
                if (columnIndex == 4) {

                    return 'font-weight:bold;color:#E6A23C'
                }
            }else  if (row.user_activity_status == "审核未通过") {
                if (columnIndex == 4) {

                    return 'font-weight:bold;color:#F56C6C'
                }
            }
            else  if (row.user_activity_status == "审核通过") {
                if (columnIndex == 4) {

                    return 'font-weight:bold;color:#67C23A'
                }
            }
        },
        activity_user_list:function(){

            let url = location.search; //这一条语句获取了包括问号开始到参数的最后，不包括前面的路径
            let params = url.substr(1);//去掉问号
            let pa = params.split("&");
            let s = new Object();
            console.log(s)

            for(let i = 0; i < pa.length; i ++){
                s[pa[i].split("=")[0]] = unescape(pa[i].split("=")[1]);
            }
            this.activity_id=s.activity_id

            console.log(this.activity_id)
            let that =this
            axios({
                method: 'post',
                url: 'https://bangbangtang.club/api/manager/activity_user_list',
                data: this.activity_id,
                headers: {'Content-Type': 'multipart/form-data'},

            })
                .then(function (ret) {
                    console.log(ret)
                    that.tableUser=ret.data['msg']

                    for(let item in that.tableUser){
                        if(that.tableUser[item]["user_activity_status"]==0) {
                            that.tableUser[item]["user_activity_status"] = "待上传结果"
                        }else if(that.tableUser[item]["user_activity_status"]==1){
                            that.tableUser[item]["user_activity_status"] = "待审核"
                        }
                        else if(that.tableUser[item]["user_activity_status"]==2){
                            that.tableUser[item]["user_activity_status"] = "审核未通过"
                        }
                        else if(that.tableUser[item]["user_activity_status"]==3){
                            that.tableUser[item]["user_activity_status"] = "审核通过"
                        }

                    }
                    console.log(that.tableUser)
                    let tableUser=that.tableUser

                })
                .catch(function (err) {
                    console.log(err)
                })
        },
        //审核通过
        activity_user_result_success(index, row){
            console.log(row["user_id"])
            let param =new FormData()

            param.append('user_id',row["user_id"])
            param.append('activity_id',this.activity_id)
            param.append('result',1)
            axios({
                method: 'post',
                url: 'https://bangbangtang.club/api/manager/activity_user_status',
                data: param,
                headers: {'Content-Type': 'multipart/form-data'},

            })
                .then(function (ret) {
                    console.log(ret)

                })
                .catch(function (err) {
                    console.log(err)
                })
        },
        //审核失败
        activity_user_result_fail(index, row){
            console.log(row["user_id"])
            let param =new FormData()

            param.append('user_id',row["user_id"])
            param.append('activity_id',this.activity_id)
            param.append('result',0)
            axios({
                method: 'post',
                url: 'https://bangbangtang.club/api/manager/activity_user_status',
                data: param,
                headers: {'Content-Type': 'multipart/form-data'},

            })
                .then(function (ret) {
                    console.log(ret)

                })
                .catch(function (err) {
                    console.log(err)
                })
        },
        activity_user_upload_result(index, row){
            console.log(index,row)
            let param =new FormData()
            param.append('user_id',row["user_id"])
            param.append('activity_id',this.activity_id)
            axios({
                method: 'post',
                url: 'https://bangbangtang.club/api/manager/activity_user_uploadInformation',
                data: param,
                headers: {'Content-Type': 'multipart/form-data'},

            })
                .then(function (ret) {
                    console.log(ret)
                    let that =this
                    that.user_upload_imgs =ret.data['img_list']
                    console.log(this.user_upload_imgs)

                })
                .catch(function (err) {
                    console.log(err)
                })
        },

        //展开信息
        expendChange(row, expandedRows){
            console.log(row,expandedRows)
            let param =new FormData()
            let that =this
            param.append('user_id',row["user_id"])
            param.append('activity_id',this.activity_id)
            axios({
                method: 'post',
                url: 'https://bangbangtang.club/api/manager/activity_user_uploadInformation',
                data: param,
                headers: {'Content-Type': 'multipart/form-data'},

            })
                .then(function (ret) {
                    console.log(ret)

                    that.user_upload_img =ret.data['img_list']
                    console.log(that.user_upload_img)

                })
                .catch(function (err) {
                    console.log(err)
                })
        },
        //下载表单图片
        onSubmit() {
            var that = this;
            console.log('submit!');
            console.log(this.form)
            for (let index = 0; index < this.form.url_list_select.length; index++) {
                console.log(this.form.url_list_select[index])
                download('第' + index + '个文件', this.form.url_list_select[index]);
            }
        },
        getSummaries(param) {
            const {columns, data} = param;
            const sums = [];
            columns.forEach((column, index) => {
                if (index === 0) {
                    sums[index] = '总价';
                    return;
                }
                const values = data.map(item => Number(item[column.property]));
                if (!values.every(value => isNaN(value))) {
                    sums[index] = values.reduce((prev, curr) => {
                        const value = Number(curr);
                        if (!isNaN(value)) {
                            return prev + curr;
                        } else {
                            return prev;
                        }
                    }, 0);
                    sums[index] += ' 元';
                } else {
                    sums[index] = 'N/A';
                }
            });

            return sums;
        }
    },
})

