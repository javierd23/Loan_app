from django.contrib.auth.models import User
from django.db import models

class Forum(models.Model):
    #text fields..
    title = models.CharField(max_length=100)
    text = models.TextField()
    #date field..
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #Linking fields...
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.ManyToManyField(User, related_name="comment_owner", through="Comment")

    def __str__(self):
        return self.title

class Comment(models.Model):
    text = models.TextField(verbose_name='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

class Reply(models.Model):
    text = models.TextField(verbose_name='', max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text