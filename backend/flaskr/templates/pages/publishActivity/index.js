var app = new Vue({
    el: "#app",
    data: {
        formInline: {
            user: '',
            region: ''
        },

        form: {
            img_url: '',
            img_list: [],
            activity_name: '',
            activity_area: '',
            activity_time: '',
            activity_type: [],
            activity_users_number:'',
            activity_prize:'',
            activity_rule:'',
            activity_description:'',
            activity_form:'',
            text_item: [{
                item: '活动描述',

            }],
        },
        param:new FormData(),
        add_item: '',
        dialogImageUrl: '',
        dialogVisible: false,
        disabled: false
    },
    methods: {
        handleAvatarSuccess(res, file) {
            let _this = this;
            _this.form.img_poster = URL.createObjectURL(file.raw);
        },
        beforeAvatarUpload(file){
            let fd = new FormData();
            fd.append('file',file);//传文件
            // fd.append('srid',this.upLoadData.srid);//传其他参数
            console.log(fd,file)
            return false//屏蔽了action的默认上传
        },
        axiosPost() {
            axios.get('http://127.0.0.1:5000/api/activity_list',{data:this.form})
                .then(response => {
                    console.log(response.data)

                })

        },
        axiosUpload() {
            axios.get('http://127.0.0.1:5000/api/manager/activity_publish',{data:this.form})

                .then(response => {
                    console.log(response.data)

                })

        },
        onSubmitForm() {//表单提交的事件
            let form =this.form
            this.param.append('activity_name',form.activity_name)
            this.param.append('activity_area',form.activity_area)
            this.param.append('activity_time',form.activity_time)

            this.param.append('activity_type',form.activity_type)
            this.param.append('img_url',form.img_url)
            this.param.append('img_list',form.img_list)
            this.param.append('text_item',form.text_item)
            this.param.append('activity_users_number',form.activity_users_number)
            this.param.append('activity_prize',form.activity_prize)
            this.param.append('activity_rule',form.activity_rule)
            this.param.append('activity_description',form.activity_description)
            this.param.append('activity_form',form.activity_form)
            for(var object_item in form.text_item)
                this.param.append(form.text_item[object_item].item,form.text_item[object_item].value)
            console.log(this.param)
            axios({
                method: 'post',
                url: 'http://127.0.0.1:5000/api/manager/activity_publish',
                headers: {'Content-Type': 'multipart/form-data'},
                onUploadProgress: function (progressEvent) {
                    console.log(progressEvent)
                },
                data: this.param
            })
                .then(function (ret) {
                    console.log(ret.data)
                })
                .catch(function (err) {
                    console.log(err)
                })
            this.$alert('发布活动', '发布成功', {
                confirmButtonText: '确定',
                callback: action => {
                    this.$message({
                        type: 'info',

                    });
                }
            });
        },

        onSubmit() {
            let that = this;
            console.log('submit!');
            console.log(this.form);
            console.log(this.param)

        },
        addFormItem() {
            if(this.form.text_item.length<5) {
                let that = this;
                that.form.text_item.push({
                    item: that.add_item,
                });
            }
        },
        submitForm(formName) {
            this.$refs[formName].validate((valid) => {
                if (valid) {
                    alert('submit!');
                } else {
                    console.log('error submit!!');
                    return false;
                }
            });
        },
        resetForm(formName) {
            this.$refs[formName].resetFields();
        },

        onchange(file) {
            console.log(file);
            //创建临时的路径来展示图片
            var windowURL = window.URL || window.webkitURL;
            this.src=windowURL.createObjectURL(file.raw);
            //重新写一个表单上传的方法

            this.param.append('file', file.raw, file.name);
            let config = {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            };

            console.log(this.param)
        },
        onchangelist(file) {
            console.log(file);
            //创建临时的路径来展示图片
            var windowURL = window.URL || window.webkitURL;
            this.src=windowURL.createObjectURL(file.raw);
            //重新写一个表单上传的方法

            this.param.append(file.name, file.raw, file.name);
            let config = {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            };

            console.log(this.param)
            this.param.forEach((value, key) => {
                console.log(`key ${key}: value ${value}`);
            })
        },
        handleRemove(file) {
            console.log(file);
            this.param.delete('file')
        },
        handlePictureCardPreview(e) {
              // 上传照片
            this.dialogImageUrl = e.url;
            this.dialogVisible = true;

        },
        handleDownload(file) {
            console.log(file);
        },


    }

})
