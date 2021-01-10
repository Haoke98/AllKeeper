from django.db import models


# Create your models here.
class Video(models.Model):
    content = models.FileField(upload_to='BeansMusicVideos')
    likeCount = models.IntegerField(null=True)
    commentCount = models.IntegerField(null=True)
    shareCount = models.IntegerField(null=True)
    title = models.CharField(max_length=100, null=True)
    introduction = models.TextField(null=True)

    date = models.DateTimeField(auto_created=True)
