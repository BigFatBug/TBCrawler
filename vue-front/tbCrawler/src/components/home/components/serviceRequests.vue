<template>
  <div style="width:100%;height:100%;" id="service_request_con"></div>
</template>

<script>
  import echarts from 'echarts';

  export default {
    name: 'serviceRequests',
    mounted() {
      this.show('')
    },
    methods: {
      show(data) {
        const option = {
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'cross',
              label: {
                backgroundColor: '#6a7985'
              }
            }
          },
          grid: {
            top: '3%',
            left: '1.2%',
            right: '1%',
            bottom: '3%',
            containLabel: true
          },
          xAxis: [
            {
              type: 'category',
              boundaryGap: false,
              data: data.dayList
            }
          ],
          yAxis: [
            {
              type: 'value'
            }
          ],
          series: [
            {
              name: '好评',
              type: 'line',
              stack: '总量',
              areaStyle: {
                normal: {
                  color: '#2d8cf0'
                }
              },
              data: data.goodList
            },
            {
              name: '中评',
              type: 'line',
              stack: '总量',
              areaStyle: {
                normal: {
                  color: '#10A6FF'
                }
              },
              data: data.normalList
            },
            {
              name: '差评',
              type: 'line',
              stack: '总量',
              areaStyle: {
                normal: {
                  color: '#0C17A6'
                }
              },
              data: data.badList
            }
          ]
        };
        const serviceRequestCharts = echarts.init(document.getElementById('service_request_con'));
        serviceRequestCharts.setOption(option);

        window.addEventListener('resize', function () {
          serviceRequestCharts.resize();
        });
      }
    }
  };
</script>
