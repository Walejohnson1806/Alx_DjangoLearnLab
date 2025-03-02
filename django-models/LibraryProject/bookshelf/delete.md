from bookshelf.models import Book

book = Book(pk=1)
book.delete()

# Verify deletion
books = Book.objects.all()
print(books)  # Expected Output: <QuerySet []>