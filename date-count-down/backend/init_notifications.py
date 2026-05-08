from datetime import datetime
from app import create_app, db
from app.models.notification import Notification

app = create_app()

with app.app_context():
    # 检查是否已存在通知
    existing_count = Notification.query.filter(Notification.user_id.is_(None)).count()
    if existing_count == 0:
        # 添加系统通知
        notifications = [
            Notification(
                title='系统维护通知',
                content='尊敬的用户：\n您好！为了提供更好的服务体验，本应用将于2026年5月1日进行系统维护，预计维护时间为1天。\n维护期间，您可能无法使用部分功能，给您带来的不便敬请谅解。\n维护完成后，我们将为您提供更加稳定和优质的服务。\n感谢您的理解与支持！',
                message='系统通知：本应用将于2026年5月1日进行系统维护，预计维护时间为1天。',
                start_time=datetime(2026, 4, 25, 0, 0, 0),
                end_time=datetime(2026, 5, 2, 0, 0, 0),
                priority=10,
                type='warning'
            ),
            Notification(
                title='新版本通知',
                content='尊敬的用户：\n您好！我们很高兴地通知您，本应用V2.0版本已正式发布。\n本次更新新增了多种倒计时模板，优化了用户界面，提升了系统性能。\n请及时更新到最新版本，享受更好的使用体验。\n感谢您一直以来的支持！',
                message='新版本通知：V2.0版本已发布，新增多种倒计时模板。',
                start_time=datetime(2026, 4, 20, 0, 0, 0),
                end_time=datetime(2026, 5, 20, 0, 0, 0),
                priority=8,
                type='info'
            )
        ]
        
        db.session.add_all(notifications)
        db.session.commit()
        print('系统通知初始化成功！')
    else:
        print('系统通知已存在，跳过初始化。')