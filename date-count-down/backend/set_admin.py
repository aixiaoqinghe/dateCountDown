from app import create_app, db
from app.models.user import User

app = create_app()
app.app_context().push()

# 将指定用户设置为管理员
username = 'xiaojiayu'
user = User.query.filter_by(username=username).first()

if user:
    user.is_admin = True
    db.session.commit()
    print(f'用户{username}已成功设置为管理员！')
else:
    print(f'未找到用户{username}')