from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView # Class Based View
from django.contrib.auth import login, logout # Function Based view
from .models import Library
from .models import Book
# Create your views here.

# Function Base View For Listing all books
def list_books(request):
    books = Book.objects.all()
    context = {'book_list': books}
    return render(request, 'relationship_app/list_books.html', context)


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    

# User Registration Class base View    
# class SignupView(CreateView):
#     form_class = UserCreationForm
#     success_url = reverse_lazy("login")
#     template_name = "register.html"
    

# class CustomLoginView(LoginView):
#     template_name = 'login.html'
    
# class CustomLogoutView(LogoutView):
#     template_name = 'logout.html'

# User Registration Function base View
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Log in the user after successful registration
            return redirect("home")  # Redirect to homepage or dashboard
    
    else:
        form = UserCreationForm()
        return render(request, "relationship_app/register.html", {"form": form})
    

# User Login View (Django provides an authentication form)
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    
    else:
        form = AuthenticationForm()
        return render(request, "registration_app/login.html", {"form": form})  
def is_admin(user):
    return user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.userprofile.role == 'Librarians'

def is_member(user):
    return user.userprofile.role == 'Member'

def logout_view(request):
    logout(request)
    return redirect("login")
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")

@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")
