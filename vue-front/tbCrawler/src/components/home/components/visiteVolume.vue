<template>
  <div style="width:100%;height:100%;" id="visite_volume_con"></div>
</template>

<script>
  import echarts from 'echarts';

  export default {
    name: 'visiteVolume',
    mounted() {
    },
    methods: {
      show(data) {
        let visiteVolume = echarts.init(document.getElementById('visite_volume_con'));

        const option = {
          tooltip: {
            trigger: 'axis',
            axisPointer: {            // 坐标轴指示器，坐标轴触发有效
              type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
            }
          },
          legend: {
            data: ['好评', '中评', '差评']
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
          },
          xAxis: {
            type: 'value'
          },
          yAxis: {
            type: 'category',
            data: data.monthList
          },
          series: [
            {
              name: '差评',
              type: 'bar',
              stack: '总量',
              label: {
                normal: {
                  show: true,
                  position: 'insideRight'
                }
              },
              data: data.badList
            },
            {
              name: '中评',
              type: 'bar',
              stack: '总量',
              label: {
                normal: {
                  show: true,
                  position: 'insideRight'
                }
              },
              data: data.normalList
            },
            {
              name: '好评',
              type: 'bar',
              stack: '总量',
              label: {
                normal: {
                  show: true,
                  position: 'insideRight'
                }
              },
              data: data.goodList
            }
          ]
        };

        visiteVolume.setOption(option);

        window.addEventListener('resize', function () {
          visiteVolume.resize();
        });
      }
    }
  };
</script>
