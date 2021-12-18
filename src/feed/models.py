from tortoise import fields
from lib.models import BaseModel


class FeedPost(BaseModel):
    related_name = 'feed_feedpost'
    author = fields.ForeignKeyField('models.User')
    text = fields.TextField(null=True)
    images = fields.ManyToManyField('models.FeedPostImage', through='feedpost_to_images')
    comments = fields.ManyToManyField('models.FeedPostComment', through='feedpost_to_comments')
    likes = fields.ManyToManyField('models.FeedPostLike', through='feedpost_to_likes')
    date = fields.DatetimeField(auto_now=True)


class FeedPostImage(BaseModel):
    file_name = fields.TextField(null=True)


class FeedPostComment(BaseModel):
    author = fields.ForeignKeyField('models.User')
    text = fields.TextField()


class FeedPostLike(BaseModel):
    author = fields.ForeignKeyField('models.User')



