from django.contrib import admin

from applications.feedback.models import Comment, Favourite, Rating, Like

admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Rating)
admin.site.register(Favourite)