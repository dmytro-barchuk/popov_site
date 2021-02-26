from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post
from .forms import PostForm
from .filters import PostFilter



def home(request):
	posts = Post.objects.filter(active=True)[:3]
	context = {'posts': posts}
	return render(request, 'gallery/home.html', context)

def posts (request):
	posts = Post.objects.filter(active=True)
	myFilter = PostFilter(request.GET, queryset=posts)
	posts = myFilter.qs
	
	page = request.GET.get('page')
	paginator = Paginator(posts, 3)

	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	context = {'posts': posts, 'myFilter': myFilter}
	return render(request, 'gallery/posts.html', context)

def post (request, slug):
	post = Post.objects.get(slug=slug)
	context = {'post': post}
	return render(request, 'gallery/post.html', context)

def profile (request):
	return  render(request, 'gallery/profile.html')

def about (request):
	file_contents = dict()
	with open('static/about/about.txt', 'r', encoding="utf-8") as f:
		line = f.readline()
		line_num = 1
		while line:
			file_contents[line] = line_num
			line_num += 1
			line = f.readline()				
		context = {'file_contents': file_contents}
	return render(request, 'gallery/about.html', context)

def mail (request):
	return render(request, 'gallery/email_form.html')

""" Инструменты для добавления, удаления, изменения постов! """
@login_required(login_url='home')
def create_post(request):
	form = PostForm()

	if request.method == 'POST':
		form = PostForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
		return redirect('posts')

	context = {'form': form}
	return render(request, 'gallery/post_form.html', context)

@login_required(login_url='home')
def update_post(request, slug):
	post = Post.objects.get(slug=slug)
	form = PostForm(instance=post)

	if request.method == 'POST':
		form = PostForm(request.POST, request.FILES, instance=post)
		if form.is_valid():
			form.save()
		return redirect('posts')

	context = {'form': form}
	return render(request, 'gallery/post_form.html', context)

@login_required(login_url='home')
def delete_post(request, slug):
	post = Post.objects.get(slug=slug)

	if request.method == 'POST':
		post.delete()
		return redirect('posts')
	context = {'item': post}
	return render(request, 'gallery/delete.html', context)

def sendMail(request):

	if request.method == 'POST':

		template = render_to_string('gallery/email_template.html', {
			'name':request.POST['name'],
			'subject':request.POST['subject'],
			'from_email':request.POST['from_email'],
			'message':request.POST['message'],
			})

		# messages = request.POST['message']
		# messages += '&#010; &#010; Отримано від: ' + request.POST['name']
		# messages += ' ' + request.POST['from_email']

		email = EmailMessage(
			request.POST['subject'],
			template,
			request.POST['from_email'],			
			['python2021@yahoo.com'],			
			)
		email.send(fail_silently=False)

	return render(request, 'gallery/email_sent.html')