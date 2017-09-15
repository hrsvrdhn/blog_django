from urllib import quote_plus
from django.shortcuts import render,get_object_or_404,redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
# from django.core.mail import send_mail
import sendgrid
import os
from sendgrid.helpers.mail import *
from django.template import loader
from django.conf import settings
# Create your views here.
from emailapp.forms import EmailPostForm
from .forms import PostForm
from .models import Post
from emailapp.models import Subscribers

def posts_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	form = PostForm(request.POST or None, request.FILES or None)
	if request.method == 'POST':
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.save()
			messages.success(request, "Succesfully Created")
			return HttpResponseRedirect(instance.get_absolute_url())
		else:
			messages.error(request, "Not Successfully Created")
	# if request.method == "POST":
	# 	title = request.POST.get("content")
	# 	Post.objects.create(title=title)
	
	context = {
		"formm" : form,
	}
	return render(request, "post_form.html", context)

def posts_detail(request, slug=None):
	instance = get_object_or_404(Post, slug=slug)
	if instance.draft or instance.publish > timezone.now().date():
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	instance.visits += 1
	instance.save()
	share_string = quote_plus(instance.content)
	context = {
		"title" : instance.title,
		"instance" : instance,
		"share_string" : share_string,
		"GITHUB" : settings.GITHUB,
		"FACEBOOK" : settings.FACEBOOK,
	}
	return render(request, "post_detail.html", context)

def posts_list(request):
	form = EmailPostForm(request.POST or None)
	if form.is_valid():
		getemail = form.cleaned_data.get('user_email')
		qs = Subscribers.objects.filter(user_email__iexact=getemail)
		if qs.exists():
			messages.success(request, "You are already with us")
		else:
			obj = Subscribers.objects.create(user_email=getemail)
			html_message = loader.render_to_string(
					'../templates/message.html',
					{
						'object' : obj,
						'local' : getattr(settings,"DEBUG",False)
					}
				)
			sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)
			from_email = Email("no-reply@codebeautiful.com")
			to_email = Email(getemail)
			subject = 'Confirmation Email'
			content = Content("text/html", html_message)
			mail = Mail(from_email, subject, to_email, content)
			response = sg.client.mail.send.post(request_body=mail.get())
			if response.status_code == 202:				
				messages.success(request, "Verification Link sent to email, check in SPAM folder also")
			else:
				obj.delete()
				messages.success(request, "Sorry, try again later !")
	today = timezone.now().date()
	queryset_list = Post.objects.active()#.order_by("-timestamp")
	if request.user.is_superuser or request.user.is_staff:
		queryset_list = Post.objects.all()
	categories = {}
	total_visits = 0
	for i in queryset_list:
		if i.category=="":
			continue
		elif i.category not in categories:
			categories[i.category] = 1
		else:
			categories[i.category] += 1
		total_visits += i.visits
	query = request.GET.get('q')
	if query:
		if not query.startswith("tags:"):	
			queryset_list = queryset_list.filter(
				Q(title__icontains=query) |
				Q(content__icontains=query) |
				Q(user__first_name__icontains=query) |
				Q(category__icontains=query) 
				).distinct()
		else:
			query = query.split(":")[1]
			queryset_list = queryset_list.filter(
				Q(category__icontains=query) 
				).distinct()

	paginator = Paginator(queryset_list, 5) 
	page_request_var = 'page'
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)

	context = {
			"obj_list" : queryset,
			"title" : "Code Beautiful",
			"page_request_var" : page_request_var,
			"today" : today,
			"categories" : categories,
			"GITHUB" : settings.GITHUB,
			"FACEBOOK" : settings.FACEBOOK,
			"total_visit" : total_visits,
			'form':form,
		}

	return render(request, "post_list.html", context)


def posts_update(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Succesfully Saved")		
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"title" : instance.title,
		"instance" : instance,
		"form" : form,
	}
	return render(request, "post_form.html", context)

def posts_delete(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	instance.delete()
	messages.success(request, "Successfully Saved!")
	return redirect("posts:list")
