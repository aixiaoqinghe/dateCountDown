from app import create_app, db
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        from alembic.config import Config
        from alembic import command
        
        alembic_cfg = Config('migrations/alembic.ini')
        command.upgrade(alembic_cfg, 'head')
        print("迁移应用成功！")