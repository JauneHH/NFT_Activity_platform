
function getAjax(url) {
    var data = null;
    $.ajax({
        url: url, //json文件路径
        async: false,
        success: function (e) { //成功
            data = e
        },
        error: function (e) { //失败
            console.log('ajax加载失败')
        },
    });
    return data;
}
var vm = new Vue({
    el: '#login',
    data() {
        return {
            ruleForm: {
                name: '',
                pwd: ''
            },
            rules: {
                name: {
                    required: true,
                    message: '请输入用户名',
                    trigger: 'blur'
                },
                pwd: {
                    required: true,
                    message: '请输入密码',
                    trigger: 'blur'
                },
            },

        }
    },
    methods: {

        submitForm(formName) {

            this.$refs[formName].validate((valid) => {
                if (valid) {
                    let url = "http://localhost:63343/mq-admin-master(h5)/index.html?"  + "name=" +this.ruleForm.name   ; //进行拼接传值

                    location.href=url;

                    console.log((this.ruleForm))
                   // window.location.href = "../../index.html"
                    // axios.post("http://localhost:8888/login", this.ruleForm).then((res) => {
                    // 	console.log(res.data)
                    // 	if (res.data.code == 200) {
                    // 		window.location.href = "../mdList.html"
                    // 		sessionStorage.setItem("userId",res.data.data.id)
                    // 	}
                    // 	layer.msg(res.data.message)
                    // })
                } else {
                    console.log('error submit!!');
                    return false;
                }
            });
        },
    }
})
