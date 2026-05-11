<template>
  <div id="app">
    <!-- ✅ 添加keep-alive缓存 -->
    <keep-alive>
      <router-view v-show="$route.meta.keepAlive" />
    </keep-alive>
    <router-view v-show="!$route.meta.keepAlive" />
  </div>
</template>

<script>
export default {
  setup () {
    return {}
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: Arial, sans-serif;
}

#app {
  min-height: 100vh;
  transition: background 0.3s ease;
}
</style>
