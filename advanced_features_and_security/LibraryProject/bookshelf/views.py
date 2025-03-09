from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Book, Author
from .forms import ExampleForm

def create_groups_and_permissions():
    # Create groups
    editors_group, created = Group.objects.get_or_create(name='Editors')
    viewers_group, created = Group.objects.get_or_create(name='Viewers')
    admins_group, created = Group.objects.get_or_create(name='Admins')

    # Get the content type for the Book model
    book_content_type = ContentType.objects.get_for_model(Book)

    # Assign permissions to groups
    editors_group.permissions.add(
        Permission.objects.get(codename='can_edit', content_type=book_content_type),
        Permission.objects.get(codename='can_create', content_type=book_content_type)
    )
    viewers_group.permissions.add(
        Permission.objects.get(codename='can_view', content_type=book_content_type)
    )
    admins_group.permissions.add(
        Permission.objects.get(codename='can_view', content_type=book_content_type),
        Permission.objects.get(codename='can_create', content_type=book_content_type),
        Permission.objects.get(codename='can_edit', content_type=book_content_type),
        Permission.objects.get(codename='can_delete', content_type=book_content_type)
    )
   
def index(request):
    return render(request, template_name="bookshelf/index.html")

def book_list(request):
    books = Book.objects.all()
    context = {"books": books}
    return render(request, "bookshelf/book_list.html", context)    
    
@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request):
    if request.method == "POST":
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        author = get_object_or_404(Author, id=author_id)
        Book.objects.create(title=title, author=author)
        return redirect('bookshelf:book_list')
    authors = Author.objects.all()
    return render(request, 'bookshelf/add_book.html', {'authors': authors})

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        book.title = request.POST.get('title')
        book.author = get_object_or_404(Author, id=request.POST.get('author'))
        book.save()
        return redirect('bookshelf:book_list')
    authors = Author.objects.all()
    return render(request, 'bookshelf/edit_book.html', {'book': book, 'authors': authors})

@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        book.delete()
        return redirect('bookshelf:book_list')
    return render(request, 'bookshelf/delete_book.html', {'book': book})    
    
def search_books(request):
    form = ExampleForm()
    books = []
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data['search_query']
            books = Book.objects.filter(title__icontains=search_query)  # Safe query
    return render(request, 'bookshelf/book_list.html', {'form': form, 'books': books})