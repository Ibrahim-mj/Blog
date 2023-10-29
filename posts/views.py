from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib import messages

from .models import Post, Category

class HomeView(TemplateView):
    template_name = 'posts/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.order_by('-created_at')[:3]
        context['categories'] = Category.objects.order_by('-created_at')[:3]
        return context

class PostListView(ListView):
    """
    A view that displays a list of blog posts.

    Attributes:
        model (Post): The model that the view represents.
        template_name (str): The name of the template to render.
        context_object_name (str): The name of the context variable to use in the template.
        ordering (str): The field to use when ordering the queryset.
    """
    model = Post
    template_name = 'posts/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

class PostDetailView(DetailView):
    """
    A view that displays the details of a single blog post.

    Attributes:
        model (Post): The model that the view will use to retrieve the post data.
        template_name (str): The name of the template that will be used to render the view.
        context_object_name (str): The name of the variable that will be used to store the post data in the template context.
    """
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'

@method_decorator(csrf_exempt, name="dispatch")
class PostCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a new blog post.

    Attributes:
        model (Post): The model used for creating the post.
        template_name (str): The name of the template used for rendering the form.
    """
    model = Post
    template_name = 'posts/post_form.html'
    fields = ['title', 'content', 'image', 'category']

    def form_valid(self, form):
        """
        If the form is valid, sets the author of the post to the current user and saves the post.
        If a category is specified in the form data, creates a new category or retrieves an existing one with the same name,
        sets the category of the post to the retrieved/created category, and saves the post.
        Returns the response from the parent class's form_valid method.
        """
        form.instance.author = self.request.user
        form.instance.title = form.cleaned_data.get('title')
        form.instance.content = form.cleaned_data.get('content')
        form.instance.image = form.cleaned_data.get('image')
        category = self.request.POST.get('category')
        if category:
            category, created = Category.objects.get_or_create(name=category)
            form.instance.category = category
            form.instance.save()
            messages.success(self.request, 'Post created successfully!')
        else:
            messages.warning(self.request, 'Please select a category.')
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        If the form is invalid, displays an error message.
        Returns the response from the parent class's form_invalid method.
        """
        messages.error(self.request, 'There was an error with your submission. Please try again.')
        return super().form_invalid(form)

    def get_success_url(self):
        """
        Returns the URL to redirect to after a successful form submission.
        In this case, it redirects to the post detail page of the newly created post.
        """
        return reverse_lazy('posts:post-detail', kwargs={'pk': self.object.pk})

@method_decorator(csrf_exempt, name="dispatch")
class PostUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for updating a blog post.

    Attributes:
        model (Post): The model used for updating the post.
        template_name (str): The name of the template used for rendering the form.
    """
    model = Post
    fields = ['title', 'content', 'image', 'category']
    context_object_name = 'post'
    template_name = 'posts/post_update.html'

    def get_object(self):
        return Post.objects.get(pk=self.kwargs['pk'])

    def form_valid(self, form):
        """
        If the form is valid, sets the author of the post to the current user and saves the post.
        If a category is specified in the form data, creates a new category or retrieves an existing one with the same name,
        sets the category of the post to the retrieved/created category, and saves the post.
        Returns the response from the parent class's form_valid method.
        """
        form.instance.author = self.request.user
        form.instance.title = form.cleaned_data.get('title')
        form.instance.content = form.cleaned_data.get('content')
        form.instance.image = form.cleaned_data.get('image')
        category = self.request.POST.get('category')
        if category:
            category, created = Category.objects.get_or_create(name=category)
            form.instance.category = category
            form.instance.save()
            messages.success(self.request, 'Post updated successfully!')
        else:
            messages.warning(self.request, 'Please select a category.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """
        If the form is invalid, displays an error message.
        Returns the response from the parent class's form_invalid method.
        """
        messages.error(self.request, 'There was an error with your submission. Please try again.')
        return super().form_invalid(form)

    def get_success_url(self) -> str:
        """
        Returns the URL to redirect to after a successful form submission.
        In this case, it redirects to the post detail page of the updated post.
        """
        return reverse_lazy('posts:post-detail', kwargs={'pk': self.object.pk})
    
class PostDeleteView(DeleteView):
    """
    View for deleting a blog post.

    Attributes:
        model (Post): The model used for deleting the post.
        template_name (str): The name of the template used for rendering the confirmation form.
    """
    model = Post
    template_name = 'posts/confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('post-list')
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['obj'] = self.object
        return context

class CategoryList(ListView):
    model = Category
    template_name = 'posts/category_list.html'
    context_object_name = 'categories'
    ordering = ['-created_at']
    
class CategoryDetailView(DetailView):
    model = Category
    template_name = 'posts/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(category=context['category'].pk)
        print(context['posts'])
        return super().get_context_data(**kwargs)

class CategoryDeleteView(DeleteView):
    """
    View for deleting a blog post.

    Attributes:
        model (Post): The model used for deleting the post.
        template_name (str): The name of the template used for rendering the confirmation form.
    """
    model = Category
    template_name = 'posts/confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('category-list')
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['obj'] = self.object
        return context
