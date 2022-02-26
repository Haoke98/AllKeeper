

# Create your tests here.
import uuid

from izBasar.secret import wxOa

if __name__ == '__main__':
    # print(generateRandomStr(32))
    x = uuid.uuid4()
    print(x, len(str(x)))
    wxOa.getQr(str(x))
    # app1.parseURLSchema("weixin://dl/business/?t=aKKbayt9kEf")
    # openLink = app2.generateUrlscheme(query=f"{uuid.uuid4()}&https://1.ink", env="develop")
    # img = qrcode.make(openLink)
    # img.save("openlink.png")
    # img.show()
    # app2.parseURLSchema("weixin://dl/business/?t=TkkDUqffnlu")
