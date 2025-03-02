from bookshelf.models import Book

updated_book = Book.objects.get(pk=1)
updated_book.title = "Nineteen Eighty-Four"
updated_book.save()
print(updated_book.title)