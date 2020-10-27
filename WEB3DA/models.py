from django.db import models

from miniProgram.models import Image, MyModel


# Create your models here.
class Map(MyModel):
    name = models.CharField(max_length=50, verbose_name='贴图名称')
    # on_delete options is DO_NOTHING because it is unnecessary to delete the image used in else where.
    map = models.ForeignKey(to=Image, on_delete=models.DO_NOTHING, null=True)

    def json(self):
        return {'name': self.name, 'src': self.map.url}

    def __str__(self):
        return self.name
