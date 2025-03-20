
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, PostForm, CommentForm
from .models import Post, Comment
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import logout
from django.db.models import Q


def home(request):
    return render(request, template_name="blog/base.html")


def logout_view(request):
    logout(request)
    return render(request, 'blog/logout.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Your account has been created, {username}! You are now able to log in')
            return redirect('blog:login')
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('blog:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
    return render(request, 'blog/profile.html', {'u_form': u_form})


class PostListView(ListView):
    model = Post
    template_name = 'blog/posts.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        # This filters Post objects to include only those with a non-null published_date and orders them by published_date in descending order.
        return Post.objects.filter(published_date__isnull=False).order_by('-published_date')
    
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the current post object
        post = self.object
        # Add the comments related to the post to the context
        context['comments'] = post.comments.all()  # related_name='comments' in Comment model
        context['comment_form'] = CommentForm()  # Add the comment form to the context
        return context

    def post(self, request, *args, **kwargs):
        # Handle the comment submission
        post = self.get_object()
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post  # Assign the post to the comment
            comment.author = request.user  # Set the author to the logged-in user
            comment.save()
            return redirect('blog:post_detail', pk=post.pk)  # Redirect to the same post detail page

        # If the form is not valid, render the same page with the form errors
        context = self.get_context_data()
        context['comment_form'] = comment_form
        return self.render_to_response(context)

class PostCreateView(CreateView, LoginRequiredMixin):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'content', 'tags']
    success_url = reverse_lazy('blog:posts')
    
    def form_valid(self, form):
        # Automatically set the author of the post to the logged-in user
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(UpdateView, LoginRequiredMixin, UserPassesTestMixin):
    model = Post
    fields = ['title', 'content', 'tags']
    success_url = reverse_lazy('blog:posts')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return  self.request.user == post.author


class PostDeleteView(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url =  reverse_lazy('blog:posts')
    items_to_delete = []
    
    def test_func(self):
        post = self.get_object()
        return  self.request.user == post.author    
    
             
# @login_required
# def comment_edit(request, comment_id):
#     comment = get_object_or_404(Comment, id=comment_id)
#     if request.user != comment.author:
#         return redirect('blog:post_detail', pk=comment.post.pk)

#     if request.method == 'POST':
#         form = CommentForm(request.POST, instance=comment)
#         if form.is_valid():
#             form.save()
#             return redirect('blog:post_detail', pk=comment.post.pk)
#     else:
#         form = CommentForm(instance=comment)

#     return render(request, 'blog/comment_edit.html', {'form': form, 'comment': comment})

# @login_required
# def comment_delete(request, comment_id):
#     comment = get_object_or_404(Comment, id=comment_id)
#     if request.user == comment.author:
#         comment.delete()
#     return redirect('blog:post_detail', pk=comment.post.pk) 

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
            # Set the author of the comment to the logged-in user
            form.instance.author = self.request.user
            # Set the post_id of the form instance to the value from the URL parameters
            form.instance.post_id = self.kwargs['pk']
            # Call the parent class's form_valid method to complete the form validation process
            return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.post.pk}) 
    
    
class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.post.pk})

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.post.pk})
    

def tagged_posts(request, tag_name):
    posts = Post.objects.filter(tags__name__in=[tag_name])
    return render(request, 'blog/tagged_posts.html', { 'posts': posts, 'tag_name': tag_name })
    
def search_posts(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) | 
            Q(tags__name__icontains=query)
        ).distinct()
    else :
        posts = Post.objects.none()
    return render(request, 'blog/search_results.html', {'posts': posts, 'query': query})        
