<template>
  <div class="skeleton-container">
    <div class="skeleton-card" v-for="i in 3" :key="i">
      <div class="skeleton-days"></div>
      <div class="skeleton-info">
        <div class="skeleton-title"></div>
        <div class="skeleton-date"></div>
        <div class="skeleton-category"></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SkeletonLoader'
}
</script>

<style scoped>
.skeleton-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 300px));
  gap: 16px;
  justify-content: center;
  padding: 20px;
}

.skeleton-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 24px;
  padding: 20px 24px;
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 20px;
  position: relative;
  overflow: hidden;
}

.skeleton-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.8), transparent);
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
}

.skeleton-days {
  width: 130px;
  height: 80px;
  background: linear-gradient(135deg, #e0e0e0 0%, #f5f5f5 50%, #e0e0e0 100%);
  border-radius: 12px;
}

.skeleton-info {
  flex: 1;
}

.skeleton-title {
  height: 24px;
  background: linear-gradient(135deg, #e0e0e0 0%, #f5f5f5 50%, #e0e0e0 100%);
  border-radius: 4px;
  margin-bottom: 8px;
}

.skeleton-date {
  height: 18px;
  width: 60%;
  background: linear-gradient(135deg, #e0e0e0 0%, #f5f5f5 50%, #e0e0e0 100%);
  border-radius: 4px;
  margin-bottom: 8px;
}

.skeleton-category {
  height: 16px;
  width: 40%;
  background: linear-gradient(135deg, #e0e0e0 0%, #f5f5f5 50%, #e0e0e0 100%);
  border-radius: 4px;
}
</style>
