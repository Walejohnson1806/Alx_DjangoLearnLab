
from django.urls import path
from .views import RegisterView, LoginView, UserProfileView, FollowUserView, UnFollowUserView



urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('follow/<int:user_id>', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnFollowUserView.as_view(), name='unfollow-user')
]
