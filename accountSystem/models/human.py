import datetime

from django.db import models

from izBasar.models import BaseModel
from lib import zodiacHelper


# Create your models here.

class Human(BaseModel):
    name = models.CharField(max_length=50, verbose_name="姓名", default="未知组")
    idCardNum = models.CharField(max_length=18, verbose_name="身份证号", null=True, blank=True)
    sex = models.CharField(max_length=1, choices=(("男", "男"), ("女", "女")),
                           verbose_name="性别", null=True, blank=True)
    birthday = models.DateField(verbose_name="出生日期", null=True, blank=True)
    zodiac = models.CharField(verbose_name='星座', max_length=50, null=True, blank=True)
    birthplace = models.CharField(verbose_name="出生地", null=True, blank=True, max_length=255)
    collage = models.CharField(verbose_name="毕业院校", null=True, blank=True, max_length=100)
    WB_ID = models.CharField(max_length=50, verbose_name="微博ID", help_text="微博首页：https://weibo.com/u/{ID}", null=True,
                             blank=True)
    DY_home = models.CharField(max_length=100, verbose_name="抖音首页", help_text="抖音首页：https://www.douyin.com/user/{系统ID}",
                               null=True, blank=True)
    DY_ID = models.CharField(max_length=50, verbose_name="抖音ID", null=True, blank=True)
    license_plate_number = models.CharField(max_length=50, verbose_name="车牌号", help_text="可以通过人人查中查询到车主信息", null=True,
                                            blank=True)

    class Meta:
        verbose_name = "人"
        verbose_name_plural = "社工库"
        db_table = "accountSystem_group"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.birthday:
            self.zodiac = zodiacHelper.get_zodiac_sign(self.birthday.strftime("%Y/%m/%d"))
        if self.idCardNum:
            birthday_str = self.idCardNum[6:14]
            self.birthday = datetime.datetime.strptime(birthday_str, "%Y%m%d").date()
            self.sex = ['女', '男'][int(self.idCardNum[14])]
        else:
            if self.birthday:
                if self.sex:
                    self.idCardNum = self.birthday.strftime(f"******%Y%m%d{['女', '男'].index(self.sex)}***")
                else:
                    self.idCardNum = self.birthday.strftime("******%Y%m%d****")
            else:
                if self.sex:
                    self.idCardNum = f"**************{['女', '男'].index(self.sex)}***"
                else:
                    pass
            pass

        super().save(*args, **kwargs)