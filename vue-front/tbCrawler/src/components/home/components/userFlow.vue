<template>
  <div style="width:100%;height:100%;" :id="'user_flow_' + index"></div>
</template>

<script>
  import echarts from 'echarts';


  export default {
    props: {
      index: Number,
      data: Object
    },
    name: 'userFlow',
    data() {
      return {
        colorList: [
          '#2d8cf0',
          '#9bd598',
          '#0C17A6',
          '#ffd58f',
          '#ca1827',
          '#abd5f2',
          '#c09821',
          '#47291e',
          '#72ee51',
          '#d8cb09'
        ]
      }
    },
    methods: {
      show(data) {
        let userFlowPie = echarts.init(document.getElementById('user_flow_' + this.index));
        let myData = []
        const self = this
        Object.keys(data.dataList).forEach(function (value, index, array) {
          myData.push({
            value: data.dataList[value],
            name: value,
            itemStyle: {normal: {color: self.colorList[index % 11]}}
          })
        })
        let titleList = data.titleList
        if (titleList.length > 12){
          titleList = []
        }
        const option = {
          tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b} : {c} ({d}%)'
          },
          legend: {
            orient: 'vertical',
            left: 'right',
            data: titleList
          },
          series: [
            {
              name: data.name,
              type: 'pie',
              radius: '66%',
              center: ['50%', '60%'],
              data: myData,
              itemStyle: {
                emphasis: {
                  shadowBlur: 10,
                  shadowOffsetX: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              }
            }
          ]
        };
        userFlowPie.setOption(option);
        window.addEventListener('resize', function () {
          userFlowPie.resize();
        });
      }
    }
  }
</script>
