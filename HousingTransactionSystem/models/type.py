from django.db import models

from izBasar.models import BaseModel


class HouseType(BaseModel):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
