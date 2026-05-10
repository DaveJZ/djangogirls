from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('inventory/', views.post_list, name='post_list'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('about/', views.about, name='about'),
    path('history/', views.transaction_history, name='transaction_history'),
    path('history/clear/', views.clear_history, name='clear_history'),
]