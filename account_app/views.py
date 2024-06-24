from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render,redirect
from . import forms
from django.urls import reverse_lazy
# from django.contrib.auth.forms import  AuthenticationForm,UserChangeForm,PasswordChangeForm
from django.contrib.auth import authenticate , login ,logout,update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import FormView
from django.contrib.auth import login
from .forms import RegistrationForm  
from book_app.models import BookModel
from django.views.generic import DetailView
from django.views import View
from django.db import models 
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import comment_form
from book_app.models import CommentModel
from book_app.models import BookModel, BorrowedBook
from transaction.models import Deposit
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView

from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string


def send_transaction_email(user, amount, subject, template_name):
        message = render_to_string(template_name, {
            'user' : user,
            'amount' : amount,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()


def home(request, book_slug=None):
    # Fetch all books
    form = BookModel.objects.all()
    book1 = None
    if book_slug is not None:     
        book1 = BookModel.objects.get(slug = book_slug)           
        form = BookModel.objects.filter(tittle=book1.tittle)
    book1 = BookModel.objects.all()
    return render(request, 'home.html', {'data': form, 'data2': book1})

class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Registration completed successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "Invalid registration details")
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'register'
        return context

    
#  log in of cardview 
class log_inView(LoginView):
    template_name = 'register.html'
    
    def get_success_url(self):
         return reverse_lazy('profile')
    
    def form_valid(self, form):
        messages.success(self.request, "Log in Completed successfully")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.warning(self.request, "Invalid User and Password")
        return super().form_invalid(form)
    
    
    def get_context_data(self, **kwargs) :
        context =  super().get_context_data(**kwargs)
        context['type'] ='log_in'
        return context
    


class log_out(LogoutView):

    def get_success_url(self):
        return reverse_lazy('log_in')

    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, 'Log out successfully')
        return super().dispatch(request, *args, **kwargs)


class profileView(ListView):
    model = BookModel
    template_name = 'profile.html'
    context_object_name = 'books'


                
class detailsView(DetailView):
        model = BookModel
        template_name = 'view_details.html'
        pk_url_kwarg ='id'
        context_object_name = 'data'
     
        # comment section start here
        
        def post(self, request, *args, **kwargs):
            self.object = self.get_object()
            comment_Form = comment_form(data=self.request.POST)
            if comment_Form.is_valid():
                new_comment = comment_Form.save(commit=False)
                new_comment.book = self.object
                new_comment.save()
            return self.get(request, *args, **kwargs)

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            book = self.object
            comments = book.comments.all()  
            print(comments)
            comment_Form = comment_form()
            context['comments'] = comments
            context['comment_form'] = comment_Form
            return context




class BorrowBookView(LoginRequiredMixin, View):
    def post(self, request, book_id):
        book = get_object_or_404(BookModel, id=book_id)
        user_deposit = Deposit.objects.filter(user=request.user).aggregate(total=models.Sum('amount'))['total'] 

        if user_deposit < book.borrow_price:
            messages.error(request, "Insufficient deposit amount to borrow this book.")
            return redirect('profile')
     
        remaining_deposit = user_deposit - book.borrow_price
        Deposit.objects.create(user=request.user, amount=-book.borrow_price)
        
      
        BorrowedBook.objects.create(user=request.user, book=book , remain= remaining_deposit)
       
        messages.success(request, f"You have successfully borrowed '{book.tittle}'. Your remaining deposit is ${remaining_deposit}.")
        
        return redirect('profile')
    
    


class BorrowedBooksView(LoginRequiredMixin, ListView):
    model = BorrowedBook
    template_name = 'profile.html'
    context_object_name = 'borrowed_books'
    
    def get_queryset(self):
        
        return BorrowedBook.objects.filter(user=self.request.user)
    
  