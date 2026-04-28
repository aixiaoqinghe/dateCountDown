from app import create_app, db
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        # 导入必要的模块
        from alembic.config import Config
        from alembic import command
        
        # 加载 alembic 配置
        alembic_cfg = Config('migrations/alembic.ini')
        
        # 创建迁移脚本
        command.revision(alembic_cfg, autogenerate=True, message='Initial migration')
        print("迁移脚本创建成功！")