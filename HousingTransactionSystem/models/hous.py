from django.db import models

from izBasar.models import ModelWithShowRate
from .layout import HouseLayout
from .phone import PhoneNumber
from .price import HousePrice
from .size import HouseSize
from .type import HouseType


class House(ModelWithShowRate):
    houseType = models.ForeignKey(to=HouseType, on_delete=models.CASCADE)
    houseLayout = models.ForeignKey(to=HouseLayout, on_delete=models.CASCADE, null=True)
    # size = models.FloatField(verbose_name="占地面积(m2)", default=103)
    size = models.ForeignKey(to=HouseSize, on_delete=models.CASCADE, verbose_name="占地面积", null=True)
    price = models.ForeignKey(to=HousePrice, on_delete=models.CASCADE, null=True)
    phoneNum = models.ForeignKey(to=PhoneNumber, on_delete=models.CASCADE, null=True)
    address = models.TextField()
    descriptions = models.TextField()
    images = models.TextField(verbose_name="所有图片的url和media_id", null=True)

    def json(self):
        images_list = self.get_images_list()
        return {'houseType': self.houseType.__str__(), 'houseLayout': self.houseLayout.__str__(),
                'address': "地址：%s" % self.address,
                'descriptions': self.descriptions,
                'phoneNum': self.phoneNum.json(), 'size': "面积：%s" % self.size.__str__(),
                'price': self.price.__str__(), 'images': images_list}

    def get_images_list(self):

        text = self.images
        if text is None:
            list = []
        else:
            list = text.split(ImageInput.separator_images_info)
            res = []
            for i in list:
                res.append(i.split(ImageInput.separator_media_id_src)[1])
            list = res
        print(self, list)
        return list
