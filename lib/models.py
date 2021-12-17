from tortoise import fields
from tortoise.models import Model
from uuid import uuid4


class BaseModel(Model):
    id = fields.IntField(pk=True)
    uuid = fields.UUIDField(default=uuid4, generated=False)

    class Meta:
        abstract = True
