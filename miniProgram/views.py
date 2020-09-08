import json

from django.http import HttpResponse

# from django.http import request
from .models import kino, episode


# Create your views here.
def getAllKino(request, id):
    print(request, id)
    result = {'err_msg': "OK", 'objects': []}
    dicts = []
    if id == 0:
        kinos = kino.objects.all()
        for per in kinos:
            video_dic = {'name': per.name,
                         'cover': per.cover.url, 'id': per.id}
            dicts.append(video_dic)
    else:
        kinos = kino.objects.get(id=id)
        per = kinos
        dict_episodes = []
        episodes = episode.objects.filter(kino=per)
        for per_eposide in episodes:
            dict_episodes.append({'name': per_eposide.name, 'content_url': per_eposide.content.url})
        video_dic = {'name': per.name,
                     'cover': per.cover.url, 'id': per.id, 'eposides': dict_episodes}
        dicts.append(video_dic)
    result['objects'] = dicts
    result = json.dumps(result, ensure_ascii=False)
    return HttpResponse(result, content_type='application/json,charset=utf-8')
