# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
class Subscription(models.Model):
    subscriber = models.ForeignKey(CustomUser, related_name='subscriptions', on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, related_name='subscribers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('subscriber', 'author')

    def __str__(self):
        return f'{self.subscriber} subscribes to {self.author}'
class Block(models.Model):
    blocker = models.ForeignKey(CustomUser, related_name='blocks', on_delete=models.CASCADE, blank=True, null=True)
    blocked_user = models.ForeignKey(CustomUser, related_name='blocked_by', on_delete=models.CASCADE,blank=True, null=True)

    class Meta:
        unique_together = ('blocker', 'blocked_user')

    def __str__(self):
        return f'{self.blocker} blocks {self.blocked_user}'