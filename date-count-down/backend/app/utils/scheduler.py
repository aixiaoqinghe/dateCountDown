# backend/app/utils/scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def check_countdown_reminders(app):
    """ 定时检查倒计时到期提醒 """
    with app.app_context():
        from app.models.countdown import Countdown
        from app.models.user_notification_setting import UserNotificationSetting
        from app.models.notification import Notification
        from app import db

        try:
            now = datetime.utcnow()

            # 查询即将到期或已到期的倒计时（提前5分钟提醒）
            countdowns = Countdown.query.filter(
                Countdown.end_time <= now,
                Countdown.reminder_sent == False
            ).all()

            for countdown in countdowns:
                # 获取用户通知设置
                setting = UserNotificationSetting.query.filter_by(
                    user_id = countdown.user_id
                ).first()

                # 如果用户开启了倒计时提醒
                if setting and setting.countdown_reminder:
                    # 创建通知记录
                    notification = Notification(
                        user_id = countdown.user_id,
                        title = '倒计时结束提醒',
                        content = f'您设置的倒计时"{countdown.title}"已结束!',
                        message = f'"{countdown.title}"已结束',
                        type = 'info',
                        priority = 2
                    )
                    db.session.add(notification)
                    countdown.reminder_sent = True
            
            db.session.commit()
            logger.info(f"检查倒计时提醒完成，处理了{len(countdowns)}个倒计时")

        except Exception as e:
            logger.error(f"检查倒计时提醒失败:{e}")


def init_scheduler(app):
    """ 初始化定时任务调度器 """
    scheduler = BackgroundScheduler(timezone='Asia/Shanghai')

    # 每分钟检查一次倒计时
    scheduler.add_job(
        check_countdown_reminders,
        'interval',
        minutes=1,
        args=[app],
        id='countdown_reminder_job'
    )

    return scheduler