
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
  
    path('' , views.home , name= 'home' ),
    path('slug/<slug:book_slug>/' , views.home  , name= 'slug_name'),
    path('details/<int:id>/' , views.detailsView.as_view() , name= 'details'), 
    path('register/', views.RegisterView.as_view() , name= 'register'),
    path('log_in/', views.log_inView.as_view() , name= 'log_in'),
    path('log_out/', views.log_out.as_view() , name= 'log_out'),
    # path('profile/', views.profileView.as_view() , name= 'profile'),
    path('borrow/<int:book_id>/', views.BorrowBookView.as_view(), name='borrow_book'),
    path('profile/', views.BorrowedBooksView.as_view(), name='profile'),
]
