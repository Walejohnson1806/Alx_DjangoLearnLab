import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_models.settings")  # Change django_models to your project name
django.setup()

from relationship_app.models import Author, Library, Book, Librarian

def get_books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    book = Book.objects.filter(author=author)
    return book
    # return author.book_set.all()
    
    
   

def get_books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.books.all()
    


# Retrieve the librarian for a library
def get_librarian_for_library(library_name):
    # library = Library.objects.get(name=library_name)
    # return library.librarian
    
    library = Library.objects.get(name=library_name)
    librarian_name = Librarian.objects.get(library=library)
    return librarian_name