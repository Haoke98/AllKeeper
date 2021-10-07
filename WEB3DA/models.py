from django.db import models

# Create your models here.
from accountSystem.models.base import BaseModel
from miniProgram.models.models import Image


class Map(BaseModel):
    name = models.CharField(max_length=50, verbose_name='贴图名称')
    # on_delete options is DO_NOTHING because it is unnecessary to delete the image used in else where.

    def json(self):
        return {'name': self.name}

    def __str__(self):
        return self.name
