var app = new Vue({
    el: "#app",
    data() {
    },
    methods: {
        Download() {
            //cavas 保存图片到本地  js 实现
            //------------------------------------------------------------------------
            //1.确定图片的类型  获取到的图片格式 data:image/Png;base64,......
            var type = 'jpg';//你想要什么图片格式 就选什么吧
            var d = document.getElementById("cavasimg");
            var imgdata = d.toDataURL(type);
            //2.0 将mime-type改为image/octet-stream,强制让浏览器下载
            var fixtype = function (type) {
                type = type.toLocaleLowerCase().replace(/jpg/i, 'jpeg');
                var r = type.match(/png|jpeg|bmp|gif/)[0];
                return 'image/' + r;
            };
            imgdata = imgdata.replace(fixtype(type), 'image/octet-stream');
            //3.0 将图片保存到本地
            var savaFile = function (data, filename) {
                var save_link = document.createElementNS('http://www.w3.org/1999/xhtml', 'a');
                save_link.href = data;
                save_link.download = filename;
                var event = document.createEvent('MouseEvents');
                event.initMouseEvent('click', true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
                save_link.dispatchEvent(event);
            };
            var filename = '' + new Date().getSeconds() + '.' + type;
            //我想用当前秒是可以解决重名的问题了 不行你就换成毫秒
            savaFile(imgdata, filename);
        }
    },
    mounted() {
        $loading.hide()

        //canvas 绘制图片    支持手机端
//            var canvas = document.getElementById('cavasimg');
//            var ctx = canvas.getContext('2d');
//            ctx.fillRect(0, 0, canvas.width, canvas.height);
//            ctx.fillStyle = "red";
//            ctx.font = 'italic bold 30px Helvetica ';
//            ctx.fillText('楷体', 50, 50);
        // canvas 插入图片   手机端点击没反应
        //获取canvas元素
        var cvs = document.getElementById("cavasimg");
        //创建image对象
        var imgObj = new Image();
        imgObj.src = "https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg";
        imgObj.setAttribute("crossOrigin", 'Anonymous')
        //待图片加载完后，将其显示在canvas上
        imgObj.onload = function () {
            var ctx = cvs.getContext('2d');
            ctx.drawImage(this, 0, 0);//this即是imgObj,保持图片的原始大小：470*480
            //ctx.drawImage(this, 0, 0,1024,768);//改变图片的大小到1024*768
        }

    }


})
