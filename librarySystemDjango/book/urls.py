from . import views
from django.urls import path, include

app_name = 'books'

urlpatterns = [
    path('', views.main_book_page, name='main_books_page'),
    path('book/<str:book_title>/', views.book_info, name='book_info_page'),
    path('book/download/<path:filename>/', views.download_file, name='dwnld_book'),
    path('add-book/', views.add_book, name='add_books'),
]