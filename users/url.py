from django.urls import path, include

from users.views import UserListView, UserDetailView, UserCreateView, UserUpdateView, UserDeleteView

urlpatterns = [
    path('', UserListView.as_view()),
    path('<int:pk>/', UserDetailView.as_view()),
    path('create/', UserCreateView.as_view()),
    path('update/<int:pk>/', UserUpdateView.as_view()),
    path('delete/<int:pk>/', UserDeleteView.as_view()),
]