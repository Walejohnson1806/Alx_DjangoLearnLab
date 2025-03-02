from bookshelf.models import Book


book = Book.objects.create(title = "1984", author = "George Orwell", publication_year = 1949)
print(book)

# book = Book()
# book.title = "1984"
# book.author = "George Orwell"
# book.publication_year = 1949
# book.save()
# print(book)  # Expected Output: <Book: 1984>