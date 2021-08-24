from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .decorators import *
from django.db.models import Q

from .forms import PostForm, CustomUserCreationForm, ProfileForm, UserForm
from .filters import PostFilter

from .models import *

# Create your views here.

def home(request):
    posts = Post.objects.filter(active=True, featured=True)[0:3]

    context = {'posts': posts}
    return render(request, 'company/Home.html', context)

def detail(request, category_slug, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.ACTIVE)
    context = {'post': post}
    return render(request, 'company/detail.html', context)

def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = category.posts.filter(status=Post.ACTIVE)
    object_list = Category.objects.all()

    context = {
        'category': category,
        'posts': posts,
        'object_list': object_list
    }


    return render(request, 'company/category.html', context )


def posts(request):

    posts = Post.objects.filter(active=True)
    myFilter = PostFilter(request.GET, queryset=posts)
    posts = myFilter.qs

    page = request.GET.get('page')
    paginator = Paginator(posts, 6)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {'posts': posts, 'myFilter': myFilter}
    return render(request, 'company/Posts.html', context)

def post(request, category_slug, slug):
    post = Post.objects.get(slug=slug)

    if request.method == 'POST':
        PostComment.objects.create(
            author=request.user.profile,
            post=post,
            body=request.POST['comment']
        )
        messages.success(request, "You're comment was succesfull posted")
        return redirect('post', slug=post.slug)
    context = {'post': post}

    return render(request, 'company/Post.html', context)



#CRUD VIEWS
@admin_only
@login_required(login_url="home")
def createPost(request):

    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('posts')

    context = {'form': form}
    return render(request, 'company/post_form.html', context)


@admin_only
@login_required(login_url="home")
def updatePost(request, slug):
    post = Post.objects.get(slug=slug)
    form = PostForm(instance=post)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
        return redirect('posts')

    context = {'form': form}
    return render(request, 'company/post_form.html', context)

@admin_only
@login_required(login_url="home")
def deletePost(request, slug):
    post = Post.objects.get(slug=slug)

    if request.method == 'POST':
        post.delete()
        return redirect('posts')
    context = {'item':post}
    return render(request, 'company/delete.html', context)

def contact_us(request):

    return render(request, 'company/contact.html')


def sendEmail(request):

    if request.method == 'POST':

        template = render_to_string('company/email_template.html', {
            'name':request.POST['name'],
            'email':request.POST['email'],
            'message':request.POST['message'],
        })

        email = EmailMessage(
            request.POST['subject'],
            template,
            settings.EMAIL_HOST_USER,
            ['snipherblog@gmail.com']
        )

        email.fail_silently=False
        email.send()

    return render(request, 'company/email_sent.html')

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password =request.POST.get('password')

        #Little Hack to work around re-building the usermodel
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except:
            messages.error(request, 'User with this email does not exists')
            return redirect('login')

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email OR password is incorrect')

    context = {}
    return render(request, 'company/login.html', context)

def registerPage(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, 'Account successfuly created!')

            user = authenticate(request, username=user.username, password=request.POST['password1'])

            if user is not None:
                login(request, user)

            next_url = request.GET.get('next')
            if next_url == '' or next_url == None:
                next_url = 'home'
            return redirect(next_url)
        else:
            messages.error(request, 'An error has occured with registration')
    context = {'form':form}
    return render(request, 'company/register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required(login_url="home")
def userAccount(request):
    profile = request.user.profile

    context = {'profile': profile}
    return render(request, 'company/account.html', context)

@login_required(login_url="home")
def updateProfile(request):
    user = request.user
    profile = user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()

        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')


    context = {'form':form}
    return render(request, 'company/profile_form.html', context)

def search(request):
    query = request.GET.get('query', '')

    posts = Post.objects.filter(status=Post.ACTIVE).filter(Q(headline__icontains=query) |
                                                           Q(sub_headline__icontains=query) |
                                                           Q(intro__icontains=query) |
                                                           Q(body__icontains=query))

    context = {
        'posts': posts,
        'query': query
    }

    return render(request, 'company/search.html', context )
