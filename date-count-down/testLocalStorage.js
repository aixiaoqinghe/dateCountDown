// 测试localStorage功能
console.log('开始测试localStorage');

// 测试写入数据
const testData = [
    {
        id: Date.now(),
        taskName: '测试任务',
        targetDate: '2023-12-31',
        category: 'test',
        createdAt: new Date().toISOString()
    }
];

console.log('写入测试数据:', testData);
try {
    localStorage.setItem('countdownHistory', JSON.stringify(testData));
    console.log('写入成功');
} catch (error) {
    console.error('写入失败:', error);
}

// 测试读取数据
try {
    const data = localStorage.getItem('countdownHistory');
    console.log('读取数据:', data);
    if (data) {
        const parsedData = JSON.parse(data);
        console.log('解析后的数据:', parsedData);
    }
} catch (error) {
    console.error('读取失败:', error);
}

// 测试清除数据
try {
    localStorage.removeItem('countdownHistory');
    console.log('清除数据成功');
    const dataAfterClear = localStorage.getItem('countdownHistory');
    console.log('清除后的数据:', dataAfterClear);
} catch (error) {
    console.error('清除失败:', error);
}