from tortoise import fields
from tortoise.models import Model
from uuid import uuid4

from hashlib import md5


class BaseModel(Model):
    id = fields.IntField(pk=True)
    uuid = fields.UUIDField(default=uuid4, generated=False)

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
