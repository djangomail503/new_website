from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from django.core.mail import send_mail
import random
from django.conf import settings
from django.http import HttpResponse
from django. contrib. auth import authenticate, login, logout

from django.views.generic import (CreateView, ListView,
                                    DetailView, UpdateView, 
                                    DeleteView)
from . import models   

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
# Create your views here.
def index(request):
    return render(request, 'base.html')

instance=0
def verify_otp(request):
    if request.method=='POST':
        otp = request.POST.get('otp')
        entr_otp = request.POST.get('entr_otp')
        if otp == entr_otp:
            instance.save()
            return HttpResponse("<h1>Registration Successfull</h1>")
  
def register_user(request):
    if request.method=='POST':
        form = forms.UserRegisterForm(request.POST)
        if form.is_valid():
            global instance
            instance = form.save(commit=False)
            instance.set_password(request.POST.get('password'))
            otp = random.randint(1111,9999)
            to_mail = request.POST.get('email')
            send_mail(
                        'Otp Verification Blog App',
                        f'Here is your otp {otp}.',
                        settings.EMAIL_HOST_USER,
                        [to_mail],
                        fail_silently=False,
                    )

            return render(request, 'registration/otp_verify.html',{'otp':otp})



    else:
        form = forms.UserRegisterForm()
        return render(request, 'registration/register.html', {'form':form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password = password)
        if user:
            login(request, user)
            request.session['log_user'] = username
            return HttpResponse("<h1>Login Successful!!!</h1>")
        else:
            return HttpResponse("<h1>Invalid Credentials!!!</h1>")
    else:
        return render(request, 'registration/login.html')

def user_logout(request):
    del request.session['log_user']
    logout(request)
    return redirect('blog:index')
###################################################
class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = models.Post
    fields = ('author', 'title','image', 'text')
    # post_form.html template/blog_app

    def form_valid(self, form):
        instance = form.save(commit=False)
        username = self.request.session['log_user']
        user = get_object_or_404(models.User, username=username)
        
        if form.is_valid():
            if instance.author == user:
                return super().form_valid(form)
            else:
                return HttpResponse("<h1>Enter Your Valid Username</h1>")
        else:
            return HttpResponse("<h1>Enter Your Valid Input</h1>")

class PostListView(ListView):
    model = models.Post
    context_object_name = 'objects'

    def get_queryset(self):
        return self.model.objects.filter(published_date__isnull=False).order_by('-published_date')

class PostDraftView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    model = models.Post
    context_object_name = 'objects'

    def get_queryset(self):

        username = self.request.session['log_user']
        author = models.User.objects.get(username=username)
        return self.model.objects.filter(author = author, published_date__isnull=True).order_by('created_date')

class PostDetailView(DetailView):
    model = models.Post

class PostUpdateView(UpdateView):
    model = models.Post
    fields = ('title', 'image', 'text')

class PostDeleteView(DeleteView):
    model = models.Post
    success_url = reverse_lazy('blog:post_list')
#####################################################
def publish_post(request, pk):
    #post = models.Post.objects.get
    post = get_object_or_404(models.Post, pk=pk)
    post.publish()
    return redirect('blog:post_list')

###########################################################
def add_comment(request, pk):
    if request.method == 'POST':
        form = forms.PostCommentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.post = get_object_or_404(models.Post, pk=pk) 
            instance.save()
            return redirect('blog:post_detail', pk=pk)

    else:
        form = forms.PostCommentForm()
        return render(request, 'blog_app/comment.html', {'form':form})