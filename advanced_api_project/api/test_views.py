from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Book, Author


class BookAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.author = Author.objects.create(name='testauthor')
        self.book = Book.objects.create(title='Test Book', publication_year=2020, author=self.author)
        self.client.login(username='testuser', password='testpassword')
    
    def test_filter_books(self):
        url = reverse('api:book-list') # Ensures that the correct URL is being called
        # response = self.client.get(url, {'author': self.author.id})
        # response = self.client.get(url, {'title': 'Test Book'})
        response = self.client.get(url, {'publication_year': 2020})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
    def test_search_books(self):
        url = reverse('api:book-list')
        # response = self.client.get(url, {'author': self.author.id})
        response = self.client.get(url, {'title': 'Test Book'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  
        
    def test_order_books(self):
        url = reverse('api:book-list')
        # response = self.client.get(url, {'ordering': 'publication_year'})
        response = self.client.get(url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)      

    def test_create_book(self):
        url = reverse('api:book-create') # Ensures that the correct URL is being called
        data = {
            'title': 'New Book',
            'publication_year': 2021,
            'author': self.author.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        
    def test_update_book(self):
        url = reverse('api:book-update', args=[self.book.id])
        data = {
            'title': 'Updated Book',
            'publication_year': 2022,
            'author': self.author.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book') 
        
    def test_delete_book(self):
        url = reverse('api:book-delete', args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)       

    def test_list_books(self):
        url = reverse('api:book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)