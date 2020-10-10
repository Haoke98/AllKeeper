from django.db import models


# Create your models here.
class Map(models.Model):
    name = models.CharField(max_length=50, verbose_name='贴图名称')
    map = models.ImageField(upload_to='maps/')

    def json(self):
        return {'name': self.name, 'src': self.map.url}
