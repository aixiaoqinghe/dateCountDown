<template>
  <div id="app">
    <router-view></router-view>
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
