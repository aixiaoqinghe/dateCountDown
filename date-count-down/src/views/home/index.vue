<template>
  <div class="home-container">
    我是homeIndex
    <router-view></router-view>
    <van-tabbar v-model="active" active-color="#ee0a24" inactive-color="#000" ref="tabbar" class="tabbar-bottom">
    <van-tabbar-item to="/home" icon="wap-home-o">首页</van-tabbar-item>
    <van-tabbar-item to="/countDown" icon="apps-o">倒计时</van-tabbar-item>
    <van-tabbar-item to="/mark" icon="shopping-cart-o">商城</van-tabbar-item>
    <van-tabbar-item to="/myself" icon="user-o">我的</van-tabbar-item>
    <van-tabbar-item to="/setting" icon="setting-o">设置</van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<script>
export default {
  name: 'homeIndex',
  data () {
    return {
      active: 0
    }
  },
  watch: {
    $route (to) {
      // 保持路由和tabbar状态同步
      const path = to.path
      const index = ['/home', '/countDown', '/mark', '/myself', '/setting'].indexOf(path)
      if (index > -1) {
        this.active = index
      }
    }
  }
}
</script>

<style>
.home-container {
  position: relative;
  min-height: 100vh;
  padding-bottom: 50px;
}

.tabbar-bottom {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  display: flex;
  background-color: #fff;
}

.van-tabbar-item {
  flex: 1;
}
</style>
