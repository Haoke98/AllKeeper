# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2023/7/3
@Software: PyCharm
@disc:
======================================="""


def get_zodiac_sign(birth_date):
    zodiac_signs = ['白羊座', '金牛座', '双子座', '巨蟹座', '狮子座', '处女座', '天秤座', '天蝎座', '射手座', '摩羯座', '水瓶座', '双鱼座']
    month = int(birth_date.split('/')[1])
    day = int(birth_date.split('/')[2])

    if (month == 3 and 21 <= day <= 31) or (month == 4 and 1 <= day <= 19):
        return zodiac_signs[0]
    elif (month == 4 and 20 <= day <= 30) or (month == 5 and 1 <= day <= 20):
        return zodiac_signs[1]
    elif (month == 5 and 21 <= day <= 31) or (month == 6 and 1 <= day <= 21):
        return zodiac_signs[2]
    elif (month == 6 and 22 <= day <= 30) or (month == 7 and 1 <= day <= 22):
        return zodiac_signs[3]
    elif (month == 7 and 23 <= day <= 31) or (month == 8 and 1 <= day <= 22):
        return zodiac_signs[4]
    elif (month == 8 and 23 <= day <= 31) or (month == 9 and 1 <= day <= 22):
        return zodiac_signs[5]
    elif (month == 9 and 23 <= day <= 30) or (month == 10 and 1 <= day <= 23):
        return zodiac_signs[6]
    elif (month == 10 and 24 <= day <= 31) or (month == 11 and 1 <= day <= 22):
        return zodiac_signs[7]
    elif (month == 11 and 23 <= day <= 30) or (month == 12 and 1 <= day <= 21):
        return zodiac_signs[8]
    elif (month == 12 and 22 <= day <= 31) or (month == 1 and 1 <= day <= 19):
        return zodiac_signs[9]
    elif (month == 1 and 20 <= day <= 31) or (month == 2 and 1 <= day <= 18):
        return zodiac_signs[10]
    elif (month == 2 and 19 <= day <= 29) or (month == 3 and 1 <= day <= 20):
        return zodiac_signs[11]
    else:
        return "无效的日期"
