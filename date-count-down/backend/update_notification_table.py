from app import create_app, db
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        # 添加新字段
        db.session.execute(text("ALTER TABLE notification ADD COLUMN message VARCHAR(500)"))
        db.session.execute(text("ALTER TABLE notification ADD COLUMN start_time DATETIME"))
        db.session.execute(text("ALTER TABLE notification ADD COLUMN end_time DATETIME"))
        db.session.execute(text("ALTER TABLE notification ADD COLUMN priority INT DEFAULT 0"))
        # 修改 user_id 允许为 NULL
        db.session.execute(text("ALTER TABLE notification MODIFY COLUMN user_id INT NULL"))
        db.session.commit()
        print('数据库表更新成功！')
    except Exception as e:
        db.session.rollback()
        print(f'更新失败：{e}')