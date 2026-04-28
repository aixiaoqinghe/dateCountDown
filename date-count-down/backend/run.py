from app import create_app, db
from flask_migrate import Migrate

# 创建Flask应用实例
app = create_app()

# 初始化数据库迁移
migrate = Migrate(app, db)

if __name__ == '__main__':
    # 启动应用，监听5000端口，开启调试模式
    app.run(debug = True, port=5000)