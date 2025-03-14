from django.urls import path, include
from .views import BookList, BookViewSet
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

app_name = 'api'
urlpatterns = [
   path('books/', BookList.as_view(), name='book-list'),
   path('', include(router.urls)),
   path('api/token/', obtain_auth_token, name='api_token_auth'), # Token authentication endpoint
]