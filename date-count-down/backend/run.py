from app import create_app, db
from flask_migrate import Migrate
import os
import atexit

# 创建Flask应用实例
app = create_app()

# 初始化数据库迁移
migrate = Migrate(app, db)

# 调度器锁文件路径
SCHEDULER_LOCK_FILE = 'scheduler.lock'

# 清理锁文件的函数
def cleanup_lock():
    if os.path.exists(SCHEDULER_LOCK_FILE):
        os.remove(SCHEDULER_LOCK_FILE)
        print("调度器锁文件已清理")

# 注册清理函数
atexit.register(cleanup_lock)

if __name__ == '__main__':
    # 检查调度器是否已经启动（通过锁文件）
    if not os.path.exists(SCHEDULER_LOCK_FILE):
        # 创建锁文件
        with open(SCHEDULER_LOCK_FILE, 'w') as f:
            f.write('running')
        
        # 创建并启动调度器
        from app.utils.scheduler import init_scheduler
        scheduler = init_scheduler(app)
        scheduler.start()
        print("调度器启动成功")
    else:
        print("调度器已在运行中，跳过启动")
    
    # 启动应用，监听所有网络接口，端口5000，开启调试模式
    app.run(debug=True, host='0.0.0.0', port=5000)