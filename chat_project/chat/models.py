from django.db import models

class ChatGroup(models.Model):
    name = models.CharField(max_length=255)
    #description = models.CharField(max_length=512, default="")

    def __str__(self):
        return self.name

class Message(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=50)  # Anonymous user
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}: {self.content}'
