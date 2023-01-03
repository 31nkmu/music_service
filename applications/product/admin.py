from django.contrib import admin
from django.db.models import Avg

from applications.product.models import Music, Album


class MusicAdmin(admin.ModelAdmin):

    list_display = ['id', 'title', 'singer', 'likes', 'ratings']

    @staticmethod
    def likes(obj):
        return obj.likes.filter(like=True).count()

    @staticmethod
    def ratings(obj):
        return obj.ratings.all().aggregate(Avg('rating'))['rating__avg']


admin.site.register(Music, MusicAdmin)
admin.site.register(Album)