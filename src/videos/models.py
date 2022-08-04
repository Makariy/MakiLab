from tortoise import fields
from lib.models import BaseModel


class Video(BaseModel):
    author = fields.ForeignKeyField('models.User')
    title = fields.TextField(null=True)
    description = fields.TextField(null=True)
    file_name = fields.TextField(null=False)
    preview = fields.TextField(null=False)
    views = fields.IntField(default=0, null=False)

    real_url = fields.TextField(null=True)
