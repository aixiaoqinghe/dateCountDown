# app/utils/schemas.py
from marshmallow import Schema, fields, validate, ValidationError
from datetime import datetime
# 这个Schema是marshmallow库提供的数据验证和序列化基类

class CountdownSchema(Schema):
    # 倒计时数据验证 Schema
    task_name = fields.Str(required = True, validate = validate.Length(min = 1, max = 100),
                           error_message={"required": "任务名称不能为空", "length": "任务名称长度必须在1-100之间"})
    task_date = fields.Str(required = True, error_massage = {"required": "目标日期不能为空"})
    category = fields.Str(required = True, validate = validate.Length(min = 1, max = 50),
                          error_message = {"required": "分类不能为空", "Length": "分类长度必须在1-50之间"})
    background_image = fields.Str(allow_none = True)

    @staticmethod
    def validate_target_date(value):
        # 验证目标日期格式是否正确
        try:
            datetime.fromisoformat(value)
        except ValueError:
            raise ValidationError("目标日期格式不正确，应为ISO格式（如：2026-04-28T13:51:00）")
        
# 创建Schema实例
countdown_schema = CountdownSchema()