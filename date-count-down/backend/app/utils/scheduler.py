# backend/app/utils/scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# 全局变量存储调度器实例（单例模式）
_scheduler_instance = None

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
            # 注意：由于数据库表中可能缺少 reminder_sent 字段，暂时不使用该字段过滤
            countdowns = Countdown.query.filter(
                Countdown.target_date <= now
            ).all()

            for countdown in countdowns:
                # 获取用户通知设置
                setting = UserNotificationSetting.query.filter_by(
                    user_id = countdown.user_id
                ).first()

                # 如果用户开启了倒计时提醒
                if setting and setting.countdown_reminder:
                    # 检查是否已经发送过提醒（通过通知记录判断）
                    existing_notification = Notification.query.filter_by(
                        user_id = countdown.user_id,
                        title = '倒计时结束提醒',
                        content = f'您设置的倒计时"{countdown.task_name}"已结束!'
                    ).first()
                    
                    if not existing_notification:
                        # 创建通知记录
                        notification = Notification(
                            user_id = countdown.user_id,
                            title = '倒计时结束提醒',
                            content = f'您设置的倒计时"{countdown.task_name}"已结束!',
                            message = f'"{countdown.task_name}"已结束',
                            type = 'info',
                            priority = 2
                        )
                        db.session.add(notification)
            
            db.session.commit()
            logger.info(f"检查倒计时提醒完成，处理了{len(countdowns)}个倒计时")

        except Exception as e:
            logger.error(f"检查倒计时提醒失败:{e}")


def init_scheduler(app):
    """ 初始化定时任务调度器（单例模式） """
    global _scheduler_instance
    
    # 如果已经有调度器实例，直接返回
    if _scheduler_instance is not None:
        logger.info("调度器实例已存在，跳过创建")
        return _scheduler_instance
    
    # 创建新的调度器实例
    scheduler = BackgroundScheduler(timezone='Asia/Shanghai')

    # 添加定时任务
    scheduler.add_job(
        check_countdown_reminders,
        'interval',
        minutes=1,
        args=[app],
        id='countdown_reminder_job'
    )
    logger.info("定时任务 'countdown_reminder_job' 已添加")
    
    # 保存实例引用
    _scheduler_instance = scheduler
    
    return scheduler