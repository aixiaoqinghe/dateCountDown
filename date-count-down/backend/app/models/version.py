from app import db
from datetime import datetime

class AppVersion(db.Model):
    __tablename__ = 'app_versions'

    id = db.Column(db.Integer, primary_key=True)
    version_number = db.Column(db.String(20), nullable=False, unique=True)   # 版本号， 如'1.0.0'
    is_latest = db.Column(db.Boolean, default=False)  # 是否为最新版本
    update_content = db.Column(db.Text)  # 更新内容(JSON格式或字符串)
    download_url = db.Column(db.String(500))   # 更新下载地址
    min_support_version = db.Column(db.String(20), default='1.0.0')  # 最低支持版本
    force_update = db.Column(db.Boolean, default=False)  # 是否强制更新
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'versionNumber': self.version_number,
            'isLatest': self.is_latest,
            'updateContent': self.update_content,
            'downloadUrl': self.download_url,
            'minSupportVersion': self.min_support_version,
            'forceUpdate': self.force_update,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
        }