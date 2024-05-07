from typing import Any
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Post 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView, 
    DeleteView
)


# Create your views here.
def home(request):
    context = {
        'posts' : Post.objects.all()
    }
    return render(request, 'Blogapp/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'Blogapp/home.html'
    context_object_name = 'posts'
    
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'Blogapp/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
      user = get_object_or_404(User, username = self.kwargs.get('username'))
      return Post.objects.filter(author = user). order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post                  
    # <app> / <model>_<viewtype>.html

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user  #setting the author as the logged in user before the form is submitted
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user  #setting the author as the logged in user before the form is submitted
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:   #avoid one user from updating someone elses post
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post   
    success_url = '/'               
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:   #avoid one user from deleting someone elses post
            return True
        return False



def about(request):
    return render(request, 'Blogapp/about.html', {'title' : 'About'})