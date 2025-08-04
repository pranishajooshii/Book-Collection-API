from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_google_books, name='search_google_books'),
    path('add/', views.add_to_collection, name='add_to_collection'),
    path('my-books/', views.get_user_collection, name='get_user_collection'),
    path('update/<int:collection_id>/', views.edit_user_collection, name='edit_user_collection'),
]
