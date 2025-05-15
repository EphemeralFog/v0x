from tortoise.models import Model
from tortoise import fields

class File(Model):
    id = fields.IntField(primary_key=True, unique=True, auto_increment=True)
    file_id = fields.CharField(max_length=255)
    file_name = fields.CharField(max_length=255)