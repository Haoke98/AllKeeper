import datetime

from django.db import models
from simplepro.components import fields
from simplepro.lib import pkHelper
from simplepro.models import BaseModel

from utils import zodiacHelper
from .weibo import Weibo


# Create your models here.
class Human(BaseModel):
    id = fields.CharField(max_length=48, primary_key=True, editable=False, default=pkHelper.uuid_generator)
    name = models.CharField(max_length=50, verbose_name="姓名", default="未知组")
    idCardNum = models.CharField(max_length=18, verbose_name="身份证号", null=True, blank=True)
    sex = models.CharField(max_length=1, choices=(("男", "男"), ("女", "女")),
                           verbose_name="性别", null=True, blank=True)
    ethnic = models.CharField(max_length=50, verbose_name="民族", null=True, blank=True)
    birthday = models.DateField(verbose_name="出生日期", null=True, blank=True)
    zodiac = models.CharField(verbose_name='星座', max_length=50, null=True, blank=True)
    birthplace = models.CharField(verbose_name="出生地", null=True, blank=True, max_length=255)
    collage = models.CharField(verbose_name="毕业院校", null=True, blank=True, max_length=100)
    WB = models.ForeignKey(to=Weibo, on_delete=models.CASCADE, null=True, blank=True, verbose_name="微博账号",
                           help_text="微博首页：https://weibo.com/u/{ID}")
    DY_home = models.CharField(max_length=255, verbose_name="抖音首页", help_text="抖音首页：https://www.douyin.com/user/{系统ID}",
                               null=True, blank=True, unique=True)
    DY_ID = models.CharField(max_length=255, verbose_name="抖音ID", null=True, blank=True, unique=True)
    license_plate_number = models.CharField(max_length=50, verbose_name="车牌号", help_text="可以通过人人查中查询到车主信息", null=True,
                                            blank=True, unique=True)
    face = fields.ImageField(verbose_name='人脸图', null=True, blank=True)
    id_card_front = fields.ImageField(verbose_name='身份证正面',
                                      max_length=128, null=True, blank=True)
    id_card_back = fields.ImageField(verbose_name='身份证反面',
                                     max_length=128, null=True, blank=True)

    class Meta:
        verbose_name = "人"
        verbose_name_plural = "社工库"
        db_table = "accountSystem_group"
        unique_together = ['name', 'idCardNum']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.birthday:
            self.zodiac = zodiacHelper.get_zodiac_sign(self.birthday.strftime("%Y/%m/%d"))
        if self.idCardNum:
            if self.birthday:
                birthday_str = self.idCardNum[6:14]
                if "*" in birthday_str:
                    self.idCardNum = self.idCardNum[0:6] + self.birthday.strftime("%Y%m%d") + self.idCardNum[14:]
            else:
                birthday_str = self.idCardNum[6:14]
                if "*" not in birthday_str:
                    self.birthday = datetime.datetime.strptime(birthday_str, "%Y%m%d").date()
                    self.zodiac = zodiacHelper.get_zodiac_sign(self.birthday.strftime("%Y/%m/%d"))
            if self.idCardNum[16] == "*":
                pass
            else:
                if int(self.idCardNum[16]) % 2 == 0:
                    self.sex = '女'  # 偶数
                else:
                    self.sex = '男'  # 奇数
        else:
            if self.birthday:
                self.idCardNum = self.birthday.strftime("******%Y%m%d****")
            else:
                pass
        super().save(*args, **kwargs)
