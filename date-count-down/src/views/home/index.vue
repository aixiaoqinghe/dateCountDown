<template>
  <div class="home-container">
    <router-view></router-view>
    <van-tabbar v-model="active" active-color="#ee0a24" inactive-color="#000" ref="tabbar" class="tabbar-bottom">
    <van-tabbar-item to="/home" icon="wap-home">首页</van-tabbar-item>
    <van-tabbar-item to="/home/countDown" icon="clock">倒计时</van-tabbar-item>
    <van-tabbar-item to="/home/mark" icon="shopping-cart">商城</van-tabbar-item>
    <van-tabbar-item to="/home/myself" icon="user">我的</van-tabbar-item>
    <van-tabbar-item to="/home/setting" icon="setting">设置</van-tabbar-item>
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
      const index = ['/home', '/home/countDown', '/home/mark', '/home/myself', '/home/setting'].indexOf(path)
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
  padding-bottom: 65px; /* 为固定定位的tabbar留出空间 */
}

.tabbar-bottom {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  display: flex;
  background-color: #fff;
  /* 增加tabbar的高度 */
  height: 65px;
  /* 增加底部阴影效果 */
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
}

.van-tabbar-item {
  flex: 1;
  /* 确保每个item有足够的空间显示图标和文字 */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

/* 增加图标大小 */
.van-tabbar-item__icon {
  font-size: 26px;
  margin-bottom: 4px;
}

/* 增加文字大小 */
.van-tabbar-item__text {
  font-size: 14px;
  line-height: 1;
}
</style>
