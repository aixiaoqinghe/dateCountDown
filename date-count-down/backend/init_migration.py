from app import create_app, db
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    from flask_migrate import init
    with app.app_context():
        init(directory='migrations')
        print("迁移环境初始化成功！")