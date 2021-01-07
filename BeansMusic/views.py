from django.http import HttpResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from .models import *


@csrf_exempt
def uploadVideo(request):
    if request.method == 'POST':
        # server_id = request.POST['server_id']
        # incident = get_object_or_404(Incident, pk=server_id)

        # imagePath = '/Library/WebServer/program/uploads/' + str(int(time.time() * 1000)) + '.jpg'
        # videoPath =
        # destination = open(imagePath, 'wb+')
        # for chunk in request.FILES['image'].chunks():
        #         destination.write(chunk)
        # destination.close()
        video = Video(content=request.FILES['video'])
        video.save()
        return HttpResponse("ok")
        # incident.ImagePath = imagePath
        # incident.save()
        # return render_to_response('webservice/incident_read.html', {'incident': incident, 'device': incident.device})
        # return
