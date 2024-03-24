from django.urls import path
from edusystem import views

urlpatterns = [
    path('products/', views.ProductListApi.as_view(), name='products'),
    path('products/<int:pk>/', views.LessonListApi.as_view(), name='lessons_by_product'),
]
