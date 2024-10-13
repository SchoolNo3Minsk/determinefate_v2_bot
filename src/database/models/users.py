from tortoise import fields
from tortoise.models import Model


class Users(Model):
    id = fields.IntField(pk=True)
    uid = fields.BigIntField(max_length=32, null=False)

    language = fields.CharField(max_length=2, null=False)

    class Meta:
        table = "users"
