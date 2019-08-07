from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm, PostForm, EmailForm
from .models import Post
import smtplib
from django.core.mail import send_mail
from django.contrib.auth.models import User





def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})



def register(request):
    if request.method == "POST":
        print("POST")
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/login")
    else:
        print("NOT POST")
        form = RegisterForm()

    return render(request, 'register/register.html', {"form": form})





def yourprofile(req):
    user = authenticate(username='danii', password='Dantous201')
    if user.is_active:
        answer = "Online"
    else:
        answer = "Offline"
    return render(req, 'blog/my_profile.html', {'answer': answer})


def password_res(req):
    return render(req, 'registration/password_reset_form.html')

def send_email_function(user, email, text):
    # user_email можешь сохранить только для того чтоб после отсылать обратно
    send_mail(
        '{}'.format(user),
        '{}'.format(text),
        '{}'.format(email),
        ['daniil.sob56@gmail.com']
    )



def contact_us(request):
    if request.method == "POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            message = form.cleaned_data.get('message')
            send_email_function(user, email, message)
            return render(request, 'blog/sent_successfully.html')

    else:
        form = EmailForm()
        print("NOT POST")

    return render(request, 'blog/contact.html', {'forms': form})





