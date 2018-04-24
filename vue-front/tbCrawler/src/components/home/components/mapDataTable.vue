<template>
    <div :style="styleObj">
        <Table border :height="240" :columns="columns" :data="cityData"></Table>
        <Page :total="100" class="margin-top-8"></Page>
    </div>
</template>

<script>
export default {
    name: 'mapDataTable',
    data () {
        return {
            columns: [
                {
                    title: '编号',
                    key: 'name'
                },
                {
                    title: '流量(k)',
                    key: 'value',
                    sortable: true
                }
            ]
        };
    },
    props: {
        cityData: Array,
        styleObj: Object
    }
};
</script>
