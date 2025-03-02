from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

def is_librarians(user):
    return user.userprofile.role == 'Librarians'


@user_passes_test(is_librarians)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')