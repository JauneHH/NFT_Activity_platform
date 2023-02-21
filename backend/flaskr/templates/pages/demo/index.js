//将要进行多文件下载的mp3文件地址，以组数的形式存起来（这里只例了3个地址）
var mp3arr = ["https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg", "https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg","https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg"];

function download(name, href) {
    var a = document.createElement("a"), //创建a标签
        e = document.createEvent("MouseEvents"); //创建鼠标事件对象
    e.initEvent("click", false, false); //初始化事件对象
    a.href = href; //设置下载地址
    a.download = name; //设置下载文件名
    a.dispatchEvent(e); //给指定的元素，执行事件click事件
}
let test=null

var app = new Vue({
    el: "#app",
    data: {

        checkAll: false,
        checkedCities: [],
        cities: ['上海', '北京', '广州', '深圳'],
        isIndeterminate: true,

        fits: ['fill', 'contain', 'cover', 'none', 'scale-down'],
        url: 'https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg',
        formInline: {
            user: '',
            region: ''
        },
        form: {
            name: '',
            region: '',
            date1: '',
            date2: '',
            delivery: false,
            type: [],
            resource: '',
            desc: '',
            rule:'',
            prize:'',
            url_list:["../../img/bg1.jpg","../../img/head.jpg","../../img/bg2.jpg"],
            url_list_select:[],
        },
        img_list:["../../img/bg1.jpg","../../img/head.jpg","../../img/bg2.jpg"],
        dialogImageUrl: '',
        dialogVisible: false,
        disabled: false,
        user_areas:[],
        user_attend_date:[],


    },

    mounted(){

        this.getStatistics()

    },

    methods: {
        handleRemove(file) {
            console.log(file);
        },
        handlePictureCardPreview(file) {
            this.dialogImageUrl = file.url;
            this.dialogVisible = true;
        },
        handleDownload(file) {
            console.log(file);
        },

        getStatistics(){
            let url = location.search; //这一条语句获取了包括问号开始到参数的最后，不包括前面的路径
            let params = url.substr(1);//去掉问号
            let pa = params.split("&");
            let s = new Object();
            console.log(s)

            for(let i = 0; i < pa.length; i ++){
                s[pa[i].split("=")[0]] = unescape(pa[i].split("=")[1]);
            }
            this.activity_id=s.activity_id
            let that =this
            let param = new FormData()
            param.append('activity_id',this.activity_id)
            axios({
                method: 'post',
                url: 'https://bangbangtang.club/api/manager/activity_statistics',
                headers: {'Content-Type': 'multipart/form-data'},
                data:param,
                onUploadProgress: function (progressEvent) {
                    console.log(progressEvent)
                },
            })
                .then(function (ret) {
                    console.log(ret)
                    test=ret.data['user_areas']
                    that.user_areas=ret.data['user_areas']
                    that.user_attend_date=ret.data['user_attend_date']
                    console.log(that.user_areas,that.user_attend_date)
                    that.img_list=ret.data['img_list']
                    //初始化对象
                    let myChart = echarts.init(document.getElementById('main'));
                    let myChart_pie = echarts.init(document.getElementById('pie'));

                    //attend_date等为日期、人数表数据

                    var attend_date=[]
                    var attend_female=[]
                    var attend_male=[]
                    var attend_total=[]
                    for(let item in that.user_attend_date){
                        console.log(that.user_attend_date[item])
                        attend_date[item]=that.user_attend_date[item]['date']
                        attend_female[item]=that.user_attend_date[item]['female']
                        attend_male[item]=that.user_attend_date[item]['male']
                        attend_total[item]=that.user_attend_date[item]['total']
                    }
                    console.log(attend_date)
                    let option = {
                        title: {
                            text: '活动参与人数',
                        },
                        tooltip: {
                            trigger: 'axis',
                            axisPointer: {
                                type: 'cross',
                                crossStyle: {
                                    color: '#999'
                                }
                            }
                        },
                        toolbox: {
                            feature: {
                                dataView: {show: true, readOnly: false},
                                magicType: {show: true, type: ['line', 'bar']},
                                restore: {show: true},
                                saveAsImage: {show: true}
                            }
                        },
                        legend: {
                            data: ['男性', '女性', '总人数']
                        },
                        xAxis: [
                            {
                                type: 'category',
                                data: attend_date,
                                axisPointer: {
                                    type: 'shadow'
                                }
                            }
                        ],
                        yAxis: [
                            {
                                type: 'value',
                                name: '人数',
                                min: 0,
                                max: 20,
                                interval: 2,
                                axisLabel: {
                                    formatter: '{value} '
                                }
                            },

                        ],
                        series: [
                            {
                                name: '男性',
                                type: 'bar',
                                data: attend_male
                            },
                            {
                                name: '女性',
                                type: 'bar',
                                data: attend_female
                            },
                            {
                                name: '总人数',
                                type: 'line',
                                yAxisIndex: 0,
                                data: attend_total
                            }
                        ]
                    };
                    // 人数日期
                    myChart.setOption(option);
                    console.log(that.user_areas,'test',test)

                    let option_pie = {
                        title:{
                            text:'参与用户所来自的地区'  ,
                            left:'center'
                        },
                        tooltip: {
                            trigger: 'item',
                            formatter: '{b}: {c}人({d}%)  '
                        },
                        legend: {
                            top: 'bottom'
                        },
                        toolbox: {
                            show: true,
                            feature: {
                                mark: {show: true},
                                dataView: {show: true, readOnly: false},
                                restore: {show: true},
                                saveAsImage: {show: true}
                            }
                        },
                        series: [
                            {
                                name: '参与用户所来自的地区',
                                type: 'pie',
                                label: {
                                    position: 'inner',
                                    fontSize: 14,
                                },
                                radius: [30, 150],
                                center: ['50%', '50%'],
                                roseType: 'area',
                                itemStyle: {
                                    borderRadius: 8
                                },
                                data: test
                            }

                        ]
                    };
                    // 人数地点
                    myChart_pie.setOption(option_pie);
                })
                .catch(function (err) {
                    console.log(err)
                })


        },
        drawCharts(){
            let that =this
            let myChart = echarts.init(document.getElementById('main'));
            let myChart_pie = echarts.init(document.getElementById('pie'));
// 指定图表的配置项和数据
            let attend_date=[]

            for(let item in this.user_attend_date){
                console.log(this.user_attend_date[item])
                attend_date[item]=this.user_attend_date[item]['date']
            }
            console.log(attend_date)
            let option = {
                title: {
                    text: '活动参与人数',
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'cross',
                        crossStyle: {
                            color: '#999'
                        }
                    }
                },
                toolbox: {
                    feature: {
                        dataView: {show: true, readOnly: false},
                        magicType: {show: true, type: ['line', 'bar']},
                        restore: {show: true},
                        saveAsImage: {show: true}
                    }
                },
                legend: {
                    data: ['男性', '女性', '总人数']
                },
                xAxis: [
                    {
                        type: 'category',
                        data: this.user_attend_date['date'][0],
                        axisPointer: {
                            type: 'shadow'
                        }
                    }
                ],
                yAxis: [
                    {
                        type: 'value',
                        name: '人数',
                        min: 0,
                        max: 1000,
                        interval: 100,
                        axisLabel: {
                            formatter: '{value} '
                        }
                    },

                ],
                series: [
                    {
                        name: '男性',
                        type: 'bar',
                        data: [72, 190,289,319,449,508]
                    },
                    {
                        name: '女性',
                        type: 'bar',
                        data: [60, 106, 200,300,307,400]
                    },
                    {
                        name: '总人数',
                        type: 'line',
                        yAxisIndex: 0,
                        data: [132, 296, 489,619,747,908]
                    }
                ]
            };
// 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);

            let option_pie = {
                title:{
                    text:'参与用户所来自的地区'  ,
                    left:'center'
                },
                tooltip: {
                    trigger: 'item',
                    formatter: '{b}: {c}人({d}%)  '
                },
                legend: {
                    top: 'bottom'
                },
                toolbox: {
                    show: true,
                    feature: {
                        mark: {show: true},
                        dataView: {show: true, readOnly: false},
                        restore: {show: true},
                        saveAsImage: {show: true}
                    }
                },
                series: [
                    {
                        name: '参与用户所来自的地区',
                        type: 'pie',
                        label: {
                            position: 'inner',
                            fontSize: 14,
                        },
                        radius: [30, 150],
                        center: ['50%', '50%'],
                        roseType: 'area',
                        itemStyle: {
                            borderRadius: 8
                        },
                        data: [
                            {value: 40, name: '上海'},

                            {value: 38, name: '北京'},
                            {value: 32, name: '南京'},
                            {value: 30, name: '杭州'},
                            {value: 28, name: '广州'},
                            {value: 26, name: '深圳'},
                            {value: 22, name: '苏州'},

                        ]
                    }

                ]
            };
            myChart_pie.setOption(option_pie);

        }

    }

})

