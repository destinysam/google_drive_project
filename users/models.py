from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserTokens(models.Model):
    """
    Model to store user tokens
    """
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    access_token = models.TextField()
    refresh_token = models.TextField(null=True,blank=True)
    expires_at = models.DateTimeField()



    def __str__(self):
        return f"Token for {self.user.username}"
