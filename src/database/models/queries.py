from tortoise import fields
from tortoise.models import Model


class Queries(Model):
    id = fields.IntField(pk=True)
    uid = fields.BigIntField()

    name = fields.CharField(max_length=32)
    surname = fields.CharField(max_length=64)
    middlename = fields.CharField(max_length=64)
    year_of_birth = fields.IntField()
    rank = fields.CharField(max_length=64)
    accepter = fields.BooleanField(null=True)

    class Meta:
        table = "queries"
