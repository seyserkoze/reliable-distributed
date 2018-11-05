from django.db import models
import os


def content_file_name(instance, filename):
	ext = filename.split('.')[-1]
	filename = "%s.%s" % (instance.name, ext)
	return os.path.join('lookup', filename)

# Create your models here.
class User(models.Model):
	name = models.CharField(max_length=42)
	email = models.EmailField()
	picture = models.FileField(upload_to = content_file_name)