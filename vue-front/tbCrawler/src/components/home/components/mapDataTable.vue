<template>
  <div :style="styleObj">
    <Table border :height="240" :columns="columns" :loading="loading" :data="data"></Table>
    <Page :total="100" class="margin-top-8"></Page>
  </div>
</template>

<script>
  export default {
    name: 'mapDataTable',
    data() {
      return {
        columns: [
          {
            title: '评论编号',
            key: 'objectId'
          },
          {
            title: '评论',
            key: 'comment'
          },
          {
            title: '用户',
            key: 'user'
          },
          {
            title: '评论时间',
            key: 'commentDate'
          }
        ]
      };
    },
    props: {
      data: Array,
      styleObj: Object,
      loading: Boolean
    }
  };
</script>
