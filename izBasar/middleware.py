from miniProgram.models.models import Settings


def sadam_middleware(get_response):
    def middleware(request):
        setting = Settings.objects.get_or_create(id=1)[0]
        setting.host = "http://%s" % request.META['HTTP_HOST']
        setting.save()
        return get_response(request)

    return middleware
