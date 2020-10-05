from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=255)
    pub_date = models.DateTimeField()
    body = models.TextField()
    image = models.ImageField(upload_to='images/',null = True)
    category = models.CharField(max_length=255)
    
    def summary(self):
        return self.body[:100]
    
    def __str__(self):
        return self.title
