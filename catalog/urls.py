"""locallibrary URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
 path('',views.index, name='index'),
 path('books/',views.BookListView.as_view(),name='books'),
 path('books/<int:pk>/',views.BookDetailView.as_view(), name='book-detail'),  
 path('author/',views.AuthorListView.as_view(),name='authors'),
 path('author/<int:pk>/',views.AuthorDetailView.as_view(),name='author-detail'),   
 path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
 path('borrowed_books/',views.BooksBorrowedListView.as_view(),name='borrowed-books'),
 path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian') ,  
 path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
 path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
 path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
 path('books/create/', views.BookCreate.as_view(), name='book-create'),
 path('books/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
 path('books/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
]

