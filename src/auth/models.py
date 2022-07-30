from hashlib import md5

from tortoise import fields

from lib.models import BaseModel


class User(BaseModel):
    username = fields.CharField(max_length=36)
    password = fields.CharField(max_length=64)

    @staticmethod
    async def hash_password(password: str):
        return md5(password.encode()).hexdigest()

    @staticmethod
    async def create_user(username: str, password: str):
        return await User.create(
            username=username,
            password=await User.hash_password(password)
        )

    async def compare_password(self, password: str):
        return self.password == await User.hash_password(password)

    class Meta:
        table = 'auth_user'
