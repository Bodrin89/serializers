
from django.urls import path
from ads.views import AdListView, AdUpdateView, AdCreateView, AdDeleteView, AdImageLoadView, AdDetailView

urlpatterns = [
    path('', AdListView.as_view()),
    path('<int:pk>/', AdDetailView.as_view()),
    path('update/<int:pk>/', AdUpdateView.as_view()),
    path('create/', AdCreateView.as_view()),
    path('delete/<int:pk>/', AdDeleteView.as_view()),
    path('<int:pk>/upload_image/', AdImageLoadView.as_view()),
    ]