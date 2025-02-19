from bookshelf.models import Book

book = Book.objects.get(title="1984")
print(f"Title: {book.title}, Author: {book.author}, year: {book.publication_year})

## Expected Output: