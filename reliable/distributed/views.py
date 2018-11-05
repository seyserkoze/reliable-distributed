from django.shortcuts import render
from distributed.models import *

# Create your views here.
def home(request):

	if (request.method=="GET"):
		return render(request, 'index.html', {})

	context = {}

	name = request.POST['name']
	email = request.POST['email']
	picture = request.FILES['picture']

	new_user = User(name=name, email=email, picture=picture)
	new_user.save()
	return render(request, 'index.html', context)
