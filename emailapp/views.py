from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404
from django.core.mail import send_mail
from django.template import loader
from django.utils import timezone
from django.conf import settings
from .forms import EmailPostForm
from .models import Subscribers
# Create your views here.

# def subscribe(request):
# 	form = EmailPostForm(request.POST or None)
# 	if form.is_valid():
# 		getemail = form.cleaned_data.get('user_email')
# 		obj = Subscribers.objects.create(user_email=getemail)
# 		html_message = loader.render_to_string(
# 				'../templates/message.html',
# 				{
# 					'object' : obj,
# 				}
# 			)
# 		subject = 'Confirmation Email'
# 		message = None
# 		from_email = 'hrsvrdhn11@gmail.com'
# 		recipient_list = [getemail]
# 		send_mail(subject, message, from_email, recipient_list, fail_silently=False, auth_user=None, auth_password=None, connection=None, html_message=html_message)
# 		return HttpResponse("Confirmation Link sent to your email ,please click and confirm")
# 	return HttpResponse("nothing here")

def confirmMail(request, key=None):
	instance = get_object_or_404(Subscribers, confirmKey=key)
	instance.confirmed = True
	instance.save()
	try:
		sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)
		from_email = Email("no-reply@codebeautiful.com")
		to_email = Email("harshavardhana.619@gmail.com")
		subject = 'Hola! You have a new subscriber'
		content = Content("text/plain", "you have a new subscriber "+ instance.user_email)
		mail = Mail(from_email, subject, to_email, content)
		response = sg.client.mail.send.post(request_body=mail.get())
	except:
		pass
	return render(request, "confirm_redirect.html",{})

def UnSubscribe(request, key=None):
	instance = get_object_or_404(Subscribers, confirmKey=key)
	instance.delete()
	return render(request, "unsubscribe.html",{})
	