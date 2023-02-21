var app = new Vue({
    el: "#app",
    data: {
        form: {
            name: ''
        },
        param:"",//表单要提交的参数
        src:"https://afp.alicdn.com/afp-creative/creative/u124884735/14945f2171400c10764ab8f3468470e4.jpg" //展示图片的地址
    },
    methods: {
        onchange(file,filesList) {
            console.log(file);
            //创建临时的路径来展示图片
            var windowURL = window.URL || window.webkitURL;
            this.src=windowURL.createObjectURL(file.raw);
            //重新写一个表单上传的方法
            this.param = new FormData();
            this.param.append('file', file.raw, file.name);
            let config = {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            };

            console.log(this.param)
        },
        handleRemove(file,filesList){
            this.param.delete('file')
        },
        onSubmit(){//表单提交的事件
            let names = this.form.name;
            //下面append的东西就会到form表单数据的fields中；
            this.param.append('message', names);

            let config = {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            };
            //然后通过下面的方式把内容通过axios来传到后台
            //下面的this.$reqs 是在主js中通过Vue.prototype.$reqs = axios 来把axios赋给它;
            axios.post("http://127.0.0.1:5000/api/test_upload", this.param, config).then(function(result) {
                console.log(result);
                console.log(this.param)
            })
        }
    }
})
