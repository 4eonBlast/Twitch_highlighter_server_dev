from django.db import models

# Create your models here.


class Videos(models.Model):
    vid_url = models.CharField(max_length=128, verbose_name='VideoUrl')
    streamer_name = models.CharField(max_length=32, verbose_name='streamer')
    vid_path = models.CharField(max_length=128, verbose_name='vid_path')
    registered_dttm = models.DateTimeField(
        auto_now_add=True, verbose_name='registered_time')

    def __str__(self):
        return self.vid_url
