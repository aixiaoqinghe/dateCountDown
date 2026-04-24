<template>
  <div class="test-container">
    <h1>测试倒计时页面</h1>
    <p>这是一个测试页面，用于验证路由是否正常工作</p>
  </div>
</template>

<script>
export default {
  name: 'testCountDown'
}
</script>

<style>
.test-container {
  padding: 20px;
  text-align: center;
  min-height: 70vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

h1 {
  font-size: 32px;
  color: #2c3e50;
  margin-bottom: 20px;
}

p {
  font-size: 18px;
  color: #7f8c8d;
}
</style>
