from django.db import models


# Create your models here.
class Video(models.Model):
    content = models.FileField(upload_to='BeansMusicVideos')
    likeCount = models.IntegerField()
    commentCount = models.IntegerField()
    shareCount = models.IntegerField()
    title = models.CharField(max_length=100)
    introduction = models.TextField()

    date = models.DateTimeField(auto_created=True)
