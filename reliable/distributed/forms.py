from django import forms
from distributed.models import * 

class UploadPicForm(forms.Form):
	name = forms.CharField(max_length=42)
	email = forms.EmailField()
	picture = forms.FileInput()

	def __str__(self):
		return self.name
	