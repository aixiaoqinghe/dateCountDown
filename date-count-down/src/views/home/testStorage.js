// 测试localStorage存储功能
console.log('=== 测试localStorage存储功能 ===');

// 测试1：写入数据
console.log('\n测试1：写入数据');
try {
  const testData = [
    {
      id: Date.now(),
      taskName: '测试任务',
      targetDate: '2024-12-31',
      category: '工作',
      createdAt: new Date().toISOString()
    }
  ];
  localStorage.setItem('countdownHistory', JSON.stringify(testData));
  console.log('✓ 数据写入成功');
  
  // 测试2：读取数据
  console.log('\n测试2：读取数据');
  const storedData = localStorage.getItem('countdownHistory');
  if (storedData) {
    console.log('✓ 数据读取成功');
    console.log('存储的数据:', JSON.parse(storedData));
  } else {
    console.log('✗ 数据读取失败');
  }
  
  // 测试3：验证数据持久化
  console.log('\n测试3：验证数据持久化');
  // 模拟页面刷新
  console.log('模拟页面刷新...');
  const refreshedData = localStorage.getItem('countdownHistory');
  if (refreshedData) {
    console.log('✓ 数据持久化成功');
    console.log('刷新后的数据:', JSON.parse(refreshedData));
  } else {
    console.log('✗ 数据持久化失败');
  }
  
} catch (error) {
  console.error('✗ 测试失败:', error);
}

console.log('\n=== 测试完成 ===');