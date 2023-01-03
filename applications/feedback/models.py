from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from applications.product.models import Music, Album

User = get_user_model()


class Like(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    music = models.ForeignKey(Music, on_delete=models.CASCADE, related_name='likes')
    like = models.BooleanField(default=False)


class Rating(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    music = models.ForeignKey(Music, on_delete=models.CASCADE, related_name='ratings')
    rating = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    music = models.ForeignKey(Music, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_ad = models.DateTimeField(auto_now_add=True)


class Favourite(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourites')
    music = models.ForeignKey(Music, on_delete=models.CASCADE, related_name='favourites', null=True, blank=True)