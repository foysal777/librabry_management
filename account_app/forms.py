from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django import forms
from book_app.models import CommentModel

class RegistrationForm(UserCreationForm):  
    class Meta :
        model = User
        fields = ['username' , 'first_name' , 'last_name' , 'email']
        
        
class comment_form(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ['name' , 'email' , 'comment_here']