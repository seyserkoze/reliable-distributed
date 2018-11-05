from django.db import models

# Create your models here.
class User(models.Model):
	name = models.CharField(max_length=42)
	email = models.EmailField()
	picture = models.FileField(upload_to = 'lookup')