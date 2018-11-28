from django.shortcuts import render
from distributed.models import *
import os
import glob
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse, Http404
from django.conf import settings

currLength = len([name for name in os.listdir('../server/results/') if os.path.isfile(name)])
altLength = len([name for name in os.listdir('../backupServer/results/') if os.path.isfile(name)])


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




def fetch(request):
	tempVar = len(os.listdir('../server/results/'))
	altTempVal = len(os.listdir('../backupServer/results/'))
	global currLength
	global altLength
	if (currLength<tempVar):
		list_of_files = glob.glob('../server/results/*')
		latest_file = max(list_of_files, key=os.path.getctime)
		subject = "faceID Results"
		email_body = """Hi we have found matches, we have attached some useful files below"""
		sender = settings.EMAIL_HOST_USER

		user_name = latest_file.split('/')[-1].split('.')[0]
		print('hello')
		print (latest_file)
		recipient = [User.objects.get(name=user_name).email]

		mail = EmailMessage(subject, email_body, sender, recipient)
		mail.attach_file(latest_file)
		mail.send()
		currLength = tempVar
		return HttpResponse(" message sent")

	if (altLength<altTempVal):
		list_of_files = glob.glob('../backupServer/results/*')
		latest_file = max(list_of_files, key=os.path.getctime)
		subject = "faceID Results"
		email_body = """Hi we have found matches, we have attached some useful files below"""
		sender = settings.EMAIL_HOST_USER

		user_name = latest_file.split('/')[-1].split('.')[0]
		print('hello')
		print (latest_file)
		recipient = [User.objects.get(name=user_name).email]

		mail = EmailMessage(subject, email_body, sender, recipient)
		mail.attach_file(latest_file)
		mail.send()
		altLength = altTempVal
		return HttpResponse(" message sent")

	return HttpResponse(" message not sent")
