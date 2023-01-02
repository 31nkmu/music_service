from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Music(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='musics')
    title = models.CharField(max_length=50)
    singer = models.CharField(max_length=50)
    image = models.ImageField(upload_to='images/')
    music = models.FileField(upload_to='songs/')
    data_added = models.DateField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Album(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums')
    title = models.SlugField(max_length=50, primary_key=True, unique=True)
    singer = models.CharField(max_length=50)
    music = models.ForeignKey(Music, on_delete=models.CASCADE, related_name='albums')

    def save(self, *args, **kwargs):
        self.title = self.title.lower()
        super(Album, self).save(*args, **kwargs)

    def __str__(self):
        return self.title