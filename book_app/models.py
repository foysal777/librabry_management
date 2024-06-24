from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.
class BookModel(models.Model):
    image = models.ImageField(upload_to='book_app/', blank=True , null= True)
    tittle = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    user_review = models.CharField(max_length=30, default = 'Good')
    borrow_price = models.IntegerField()
    slug = models.SlugField(max_length=100 , unique=True,  blank=True , null= True)
    dates = models.DateTimeField(auto_now=True) 
    
    

    
    def __str__(self):
        return self.tittle
    
    

class BorrowedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(auto_now_add=True)
    return_due_date = models.DateTimeField(null=True, blank=True)
    remain = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username} borrowed {self.book.tittle}"
    
    
class CommentModel(models.Model):
    book = models.ForeignKey('BookModel', related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    email = models.EmailField()
    comment_here = models.TextField(max_length=100)
    show_date = models.DateTimeField(auto_now_add=True)      
    
    
    def __str__(self):
        return self.name