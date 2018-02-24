var myChart=echarts.init(document.getElementById('pic_chart'));
option = {
    title: {
        text: '资源图标'
    },
    tooltip: {
        trigger: 'axis'
    },
    legend: {
        data:['邮件营销','联盟广告','视频广告','直接访问','搜索引擎']
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    toolbox: {
        feature: {
            saveAsImage: {}
        }
    },
    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: ['视频资源','题库资源','点读资源']
    },
    yAxis: {
        type: 'value',
        boundaryGap: false,
        data: [0, 5000, 10000, 15000, 20000, 25000]
    },
    series: [
        {
            name:'方直科技',
            type:'line',
            stack: '总量',
            data:[5000, 10000, 15000]
        },
        {
            name:'优博视',
            type:'line',
            stack: '总量',
            data:[6000, 12000, 17000]
        },
        {
            name:'创维',
            type:'line',
            stack: '总量',
            data:[7000, 14000, 19000]
        },
    ]
};
myChart.setOption(option);