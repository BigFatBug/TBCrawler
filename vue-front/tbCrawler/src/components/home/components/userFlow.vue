<template>
  <div style="width:100%;height:100%;" id="user_flow"></div>
</template>

<script>
  import echarts from 'echarts';


  export default {
    name: 'userFlow',
    mounted() {
    },
    methods: {
      show(data) {
        let dataSourcePie = echarts.init(document.getElementById('data_source_con'));
        const option = {
          tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b} : {c} ({d}%)'
          },
          legend: {
            orient: 'vertical',
            left: 'right',
            data: ['好评', '中评', '差评']
          },
          series: [
            {
              name: '评论占比',
              type: 'pie',
              radius: '66%',
              center: ['50%', '60%'],
              data: [
                {value: data.good, name: '好评', itemStyle: {normal: {color: '#9bd598'}}},
                {value: data.normal, name: '中评', itemStyle: {normal: {color: '#ffd58f'}}},
                {value: data.bad, name: '差评', itemStyle: {normal: {color: '#abd5f2'}}}
              ],
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
        dataSourcePie.setOption(option);
        window.addEventListener('resize', function () {
          dataSourcePie.resize();
        });
      }
    }
  }
</script>
