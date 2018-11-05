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
	context['message'] = "Thank you, your information has been saved. We will send you an email at " + str(email) + " as soon as we get any updates."
	return render(request, 'index.html', context)
