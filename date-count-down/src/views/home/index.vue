<template>
  <div class="home-container">
    <router-view></router-view>
    <div class="tabbar-container">
      <van-tabbar v-model="active" active-color="#3498db" inactive-color="#999" ref="tabbar" class="tabbar-bottom">
        <van-tabbar-item to="/home" icon="wap-home" class="tabbar-item">
          <span class="tabbar-text">首页</span>
        </van-tabbar-item>
        <van-tabbar-item to="/home/countDown" icon="clock" class="tabbar-item">
          <span class="tabbar-text">倒计时</span>
        </van-tabbar-item>
        <van-tabbar-item to="/home/mark" icon="shopping-cart" class="tabbar-item">
          <span class="tabbar-text">商城</span>
        </van-tabbar-item>
        <van-tabbar-item to="/home/mine" icon="user" class="tabbar-item">
          <span class="tabbar-text">我的</span>
        </van-tabbar-item>
        <van-tabbar-item to="/home/setting" icon="setting" class="tabbar-item">
          <span class="tabbar-text">设置</span>
        </van-tabbar-item>
      </van-tabbar>
    </div>
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
      const index = ['/home', '/home/countDown', '/home/mark', '/home/mine', '/home/setting'].indexOf(path)
      if (index > -1) {
        this.active = index
      }
    }
  }
}
</script>

<style scoped>
.home-container {
  position: relative;
  min-height: 100vh;
  padding-bottom: 65px; /* 为固定定位的tabbar留出空间 */
}

.tabbar-container {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: #ffffff;
  border-top: 1px solid #f0f0f0;
  width: 100%;
}

.tabbar-bottom {
  display: flex;
  justify-content: space-around;
  background: transparent;
  height: 65px;
  box-shadow: none;
  padding: 0;
  width: 100%;
}

.tabbar-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  position: relative;
  padding: 5px 0;
  border-radius: 12px;
  margin: 0 5px;
}

.tabbar-item:active {
  background: #f8f9fa;
}

/* 图标样式 */
.van-tabbar-item__icon {
  font-size: 26px;
  margin-bottom: 6px;
  transition: all 0.3s ease;
}

/* 文字样式 */
.tabbar-text {
  font-size: 14px;
  line-height: 1;
  font-weight: 400;
  transition: all 0.3s ease;
  color: #999;
  font-family: 'PingFang SC', 'Helvetica Neue', Arial, sans-serif;
}

/* 激活状态样式 */
.van-tabbar-item--active {
  background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(52, 152, 219, 0.4);
}

.van-tabbar-item--active .van-tabbar-item__icon {
  color: #ffffff;
  transform: scale(1.2);
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.van-tabbar-item--active .tabbar-text {
  color: #ffffff;
  font-weight: 600;
  font-size: 15px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

/* 为激活项添加指示器 */
.van-tabbar-item--active::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 50%;
  transform: translateX(-50%);
  width: 30px;
  height: 4px;
  background: #ffffff;
  border-radius: 4px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .home-container {
    padding-bottom: 60px;
  }

  .tabbar-bottom {
    height: 60px;
  }

  .tabbar-item {
    margin: 0 3px;
  }

  .van-tabbar-item__icon {
    font-size: 24px;
    margin-bottom: 4px;
  }

  .tabbar-text {
    font-size: 13px;
  }

  .van-tabbar-item--active .tabbar-text {
    font-size: 14px;
  }
}

@media (min-width: 769px) {
  .home-container {
    padding-bottom: 70px;
  }

  .tabbar-bottom {
    height: 70px;
  }

  .tabbar-item {
    margin: 0 8px;
  }

  .van-tabbar-item__icon {
    font-size: 28px;
  }

  .tabbar-text {
    font-size: 15px;
  }

  .van-tabbar-item--active .tabbar-text {
    font-size: 16px;
  }
}
</style>
