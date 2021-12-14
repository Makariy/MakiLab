from tortoise.models import Model
from tortoise import fields
from hashlib import md5


class BaseModel(Model):
    id = fields.IntField(pk=True)

    class Meta:
        abstract = True


class User(BaseModel):
    username = fields.CharField(max_length=36)
    password = fields.CharField(max_length=64)

    @staticmethod
    async def create_user(username: str, password: str):
        return await User.create(
            username=username,
            password=md5(password.encode()).hexdigest()
        )

    async def compare_password(self, password: str):
        return self.password == md5(password.encode()).hexdigest()

    class Meta:
        table = 'auth_user'


class FeedPost(BaseModel):
    related_name = 'feed_feedpost'
    author = fields.ForeignKeyField('models.User', related_name=related_name)
    text = fields.TextField(null=True, default='')
    images = fields.ManyToManyField('models.FeedPostImage', related_name=related_name, through='feed_feedpost_to_images')
    comments = fields.ManyToManyField('models.FeedPostComment', related_name=related_name, through='feed_feedpost_to_comments')
    likes = fields.ManyToManyField('models.FeedPostLike', related_name=related_name, through='feed_feedpost_to_likes')
    date = fields.DatetimeField(auto_now=True)


class FeedPostImage(Model):
    file_name = fields.TextField(null=True)


class FeedPostComment(Model):
    author = fields.ForeignKeyField('models.User', null=True)
    text = fields.TextField()


class FeedPostLike(Model):
    author = fields.ForeignKeyField('models.User')



