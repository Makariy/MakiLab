from tortoise import fields
from lib.models import BaseModel, User


class Video(BaseModel):
    author = fields.ForeignKeyField('models.User')
    title = fields.TextField(null=True)
    description = fields.TextField(null=True)
    file_name = fields.TextField(null=False)
    preview = fields.ForeignKeyField('models.VideoPreview')
    views = fields.IntField(default=0, null=False)

    real_url = fields.TextField()


class VideoPreview(BaseModel):
    file_name = fields.TextField(null=False)

