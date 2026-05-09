from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
]