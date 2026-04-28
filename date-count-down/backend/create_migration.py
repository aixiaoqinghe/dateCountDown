from app import create_app, db
from flask_migrate import Migrate
from alembic.config import Config
from alembic.runtime.environment import EnvironmentContext
from alembic.script import ScriptDirectory
from alembic.autogenerate import api as autogenerate_api

app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        # 加载 alembic 配置
        alembic_cfg = Config('migrations/alembic.ini')
        script = ScriptDirectory.from_config(alembic_cfg)
        
        # 创建迁移脚本
        def upgrade(rev, context):
            return script._upgrade_revs('heads', rev)
        
        with EnvironmentContext(alembic_cfg, script, fn=upgrade):
            # 自动生成迁移脚本
            autogenerate_api.autogenerate(script, alembic_cfg, 'Initial migration')
            print("迁移脚本创建成功！")