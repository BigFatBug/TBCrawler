<style lang="less">
  @import "./home.less";

  .margin-top-8 {
    margin-top: 8px;
  }

  .margin-top-10 {
    margin-top: 10px;
  }

  .margin-top-20 {
    margin-top: 20px;
  }

  .margin-left-10 {
    margin-left: 10px;
  }

  .margin-bottom-10 {
    margin-bottom: 10px;
  }

  .margin-bottom-100 {
    margin-bottom: 100px;
  }

  .margin-right-10 {
    margin-right: 10px;
  }

  .padding-left-6 {
    padding-left: 6px;
  }

  .padding-left-8 {
    padding-left: 5px;
  }

  .padding-left-10 {
    padding-left: 10px;
  }

  .padding-left-20 {
    padding-left: 20px;
  }

  .height-100 {
    height: 100%;
  }

  .height-120px {
    height: 100px;
  }

  .height-200px {
    height: 200px;
  }

  .height-492px {
    height: 492px;
  }

  .height-460px {
    height: 460px;
  }

  .line-gray {
    height: 0;
    border-bottom: 2px solid #dcdcdc;
  }

  .notwrap {
    word-break: keep-all;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .padding-left-5 {
    padding-left: 10px;
  }

  [v-cloak] {
    display: none;
  }
</style>
<template>
  <div class="home-main">
    <Row :gutter="10">
      <Col :md="24" :lg="8">
      <Row class-name="home-page-row1" :gutter="10">
        <Col :md="12" :lg="24" :style="{marginBottom: '10px'}">
        <Card>
          <Row type="flex" class="user-infor">
            <Col span="8">
            <Row class-name="made-child-con-middle" type="flex" align="middle">
              <img class="avator-img" :src="require('../../assets/spider.jpg')"/>
            </Row>
            </Col>
            <Col span="16" style="padding-left:6px;">
            <Row class-name="made-child-con-middle" type="flex" align="middle">
              <div>
                <Input v-model="url" placeholder="输入商品链接"></Input>
                <Button type="primary" :loading="startLoading" icon="checkmark-round" class="margin-top-10"
                        @click="start">
                  <span v-if="!startLoading">开爬!</span>
                  <span v-else>爬取中...</span>
                </Button>
              </div>
            </Row>
            </Col>
          </Row>
          <div class="line-gray"></div>
          <Row class="margin-top-8">
            <Col span="8">
            <p class="notwrap">选择商城:</p></Col>
            <Col span="16" class="padding-left-8">
            <RadioGroup v-model="mall">
              <Radio :label="'taobao'">
                <Icon type="bag"></Icon>
                <span>淘宝</span>
              </Radio>
              <Radio :label="'tmail'">
                <Icon type="speakerphone"></Icon>
                <span>天猫</span>
              </Radio>
            </RadioGroup>
            </Col>
          </Row>
        </Card>
        </Col>
        <Col :md="12" :lg="24" :style="{marginBottom: '10px'}">
        <Card>
          <p slot="title" class="card-title">
            <Icon type="android-checkbox-outline"></Icon>
            用户统计
          </p>
          <a type="text" slot="extra" @click.prevent="addNewToDoItem">
            <Icon type="plus-round"></Icon>
          </a>
          <Modal
            v-model="showAddNewTodo"
            title="添加新的待办事项"
            @on-ok="addNew"
            @on-cancel="cancelAdd">
            <Row type="flex" justify="center">
              <Input v-model="newToDoItemValue" icon="compose" placeholder="请输入..." style="width: 300px"/>
            </Row>
            <Row slot="footer">
              <Button type="text" @click="cancelAdd">取消</Button>
              <Button type="primary" @click="addNew">确定</Button>
            </Row>
          </Modal>
          <div class="to-do-list-con">
            <div v-for="(item, index) in toDoList" :key="index" class="to-do-item">
              <to-do-list-item :content="item.title"></to-do-list-item>
            </div>
          </div>
        </Card>
        </Col>
      </Row>
      </Col>
      <Col :md="24" :lg="16">
      <Row :gutter="5">
        <Col v-for="tag in tagList" :xs="24" :sm="12" :md="6" :style="{marginBottom: '10px'}">
        <infor-card
          :end-val="tag.count"
          iconType="android-person-add"
          color="#2d8cf0"
          intro-text="tag.title"
        ></infor-card>
        </Col>
      </Row>
      <Row>
        <Card :padding="0">
          <p slot="title" class="card-title">
            <Icon type="map"></Icon>
            评论列表
          </p>
          <div class="map-con">
            <Col span="24">
              <map-data-table :data="rateList" height="281" :style-obj="{margin: '12px 0 0 11px'}"></map-data-table>
            </Col>
          </div>
        </Card>
      </Row>
      </Col>
    </Row>
    <Row :gutter="10" class="margin-top-10">
      <Col :md="24" :lg="8" :style="{marginBottom: '10px'}">
      <Card>
        <p slot="title" class="card-title">
          <Icon type="android-map"></Icon>
          过去半年评论数统计
        </p>
        <div class="data-source-row">
          <visite-volume ref="lastSix"></visite-volume>
        </div>
      </Card>
      </Col>
      <Col :md="24" :lg="8" :style="{marginBottom: '10px'}">
      <Card>
        <p slot="title" class="card-title">
          <Icon type="ios-pulse-strong"></Icon>
          评论比例图统计
        </p>
        <div class="data-source-row">
          <data-source-pie ref="rateWeight"></data-source-pie>
        </div>
      </Card>
      </Col>
      <Col :md="24" :lg="8">
      <Card>
        <p slot="title" class="card-title">
          <Icon type="ios-pulse-strong"></Icon>
          每日好评占比折线图
        </p>
        <div class="data-source-row">
          <user-flow></user-flow>
        </div>
      </Card>
      </Col>
    </Row>
    <Row class="margin-top-10">
      <Card>
        <p slot="title" class="card-title">
          <Icon type="ios-shuffle-strong"></Icon>
          各种评论每日比例趋势
        </p>
        <div class="line-chart-con">
          <service-requests ref="everyDay"></service-requests>
        </div>
      </Card>
    </Row>
  </div>
</template>

<script>
  import cityData from './map-data/get-city-value.js';
  import homeMap from './components/map.vue';
  import dataSourcePie from './components/dataSourcePie.vue';
  import visiteVolume from './components/visiteVolume.vue';
  import serviceRequests from './components/serviceRequests.vue';
  import userFlow from './components/userFlow.vue';
  import countUp from './components/countUp.vue';
  import inforCard from './components/inforCard.vue';
  import mapDataTable from './components/mapDataTable.vue';
  import toDoListItem from './components/toDoListItem.vue';

  export default {
    name: 'home',
    components: {
      homeMap,
      dataSourcePie,
      visiteVolume,
      serviceRequests,
      userFlow,
      countUp,
      inforCard,
      mapDataTable,
      toDoListItem
    },
    data() {
      return {
        mall: 'tmail',
        startLoading: false,
        ifTarget: true,
        toDoList: [
          {
            title: '去iView官网学习完整的iView组件'
          },
          {
            title: '去iView官网学习完整的iView组件'
          },
          {
            title: '去iView官网学习完整的iView组件'
          },
          {
            title: '去iView官网学习完整的iView组件'
          },
          {
            title: '去iView官网学习完整的iView组件'
          }
        ],
        url: '',
        objectId: '',
        tagList: [],
        rateList: []
      };
    },
    methods: {
      start() {
        this.$http.get("/start", {params: {url: this.url}}).then((response) => {
          this.objectId = response.data.objectId
          this.queryRates(objectId, 1)
          this.$http.get("/queryTags", {params: {object: this.object}}).then((response) => {
            this.tagList = response.data
          })
          this.$http.get("/queryRateTypeWeight", {params: {object: this.object}}).then((response) => {
//            this.objectId = response.data.objectId
          })
          this.$http.get("/queryLastSixMonth", {params: {object: this.object}}).then((response) => {
//            this.objectId = response.data.objectId
          })
          this.$http.get("/queryRateTypeEveryDay", {params: {object: this.object}}).then((response) => {
//            this.objectId = response.data.objectId
          })
          this.$http.get("/queryObjectTypeWeight", {params: {object: this.object}}).then((response) => {
//            this.objectId = response.data.objectId
          })
        })
      },
      queryRates(objectId, pageNum) {
        this.$http.get("/queryRates", {params: {object: this.object, pageNum: pageNum}}).then((response) => {
          this.objectId = response.data.objectId
        })
      }
    }
  };
</script>
