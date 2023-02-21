

from django.urls import path
from ads.views import CategoryDetailView, CatListView, CatCreateView, CatUpdateView, CatDeleteView

urlpatterns = [
    path('', CatListView.as_view()),
    path('<int:pk>', CategoryDetailView.as_view()),
    path('create/', CatCreateView.as_view()),
    path('update/<int:pk>/', CatUpdateView.as_view()),
    path('delete/<int:pk>/', CatDeleteView.as_view()),
    ]