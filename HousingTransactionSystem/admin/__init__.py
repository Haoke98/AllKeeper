from django.contrib import admin

from HousingTransactionSystem.models import HouseType, HouseSize, HouseLayout, PhoneNumber, HousePriceType, HousePrice, \
    HouseSizeUnit
from izBasar.admin import BaseAdmin


@admin.register(HouseType)
class HouseTypeAdmin(BaseAdmin):
    exclude = ('',)


@admin.register(HouseLayout)
class HouseLayoutAdmin(BaseAdmin):
    exclude = ('',)


@admin.register(PhoneNumber)
class PhoneNumberAdmin(BaseAdmin):
    exclude = ('',)


@admin.register(HousePriceType)
class HousePriceTypeAdmin(BaseAdmin):
    exclude = ('',)


@admin.register(HousePrice)
class HousePriceAdmin(BaseAdmin):
    exclude = ('',)


@admin.register(HouseSizeUnit)
class HouseSizeUnitAdmin(BaseAdmin):
    exclude = ('',)


@admin.register(HouseSize)
class HouseSizeAdmin(BaseAdmin):
    exclude = ('',)
