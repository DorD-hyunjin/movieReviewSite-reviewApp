from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Review(models.Model) :
    movie = models.ForeignKey('movie.Movie', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    star = models.PositiveIntegerField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    modify_date = models.DateTimeField(null=True, blank=True)  # auto_now=True
    like_review = models.ManyToManyField(User, default=0, related_name='like_review')
    unlike_review = models.ManyToManyField(User, default=0, related_name='unlike_review')
    review_hit = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    @property
    def update_counter(self):
        self.review_hit = self.review_hit +1
        self.save()