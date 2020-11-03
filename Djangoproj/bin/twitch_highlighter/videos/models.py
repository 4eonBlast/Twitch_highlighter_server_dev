from django.db import models

# Create your models here.


class Streamer(models.Model):
    streamer_name = models.CharField(
        max_length=32, verbose_name='Streamer Name')

    def __str__(self):
        return self.streamer_name

    class Meta:
        db_table = 'Streamer'
        verbose_name_plural = 'Streamer'

# me = User.objects.get(name='navill')
# # user에 user객체를 할당하면 해당 객체의 id가 user_id로 저장
# post_by_navill = Post.objects.filter(user=me)
# # 역관계
# post_by_navill = me.post_set.all()  # 1번
# post_by_navill = me.posts.all()  # 2번(related_name='posts' 설정)


class Videos(models.Model):

    streamer_name = models.ForeignKey(
        Streamer, on_delete=models.CASCADE, related_name='videos')
    vid_title = models.CharField(
        max_length=128, verbose_name='vid_title', default="Unready")
    vid_url = models.CharField(max_length=128, verbose_name='vid_url')
    vid_path = models.CharField(max_length=128, verbose_name='vid_path')
    vid_num = models.CharField(max_length=32, verbose_name='vid_num')
    vid_file = models.FileField(upload_to="media/video", null=True)
    registered_dttm = models.DateTimeField(
        auto_now_add=True, verbose_name='registered_time')

    def __str__(self):
        self_str = str(self.streamer_name) + ' '+self.vid_url
        return self_str

    class Meta:
        db_table = 'video'
        verbose_name_plural = 'video'
