
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import DepositForm
from .models import Deposit
from django.db import models 
from django.db.models import Sum
from book_app.models import BookModel, BorrowedBook
from django.views.generic import ListView
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


class DepositView(LoginRequiredMixin, FormView):
    template_name = 'deposit.html'
    form_class = DepositForm
    success_url = reverse_lazy('home')  

    def form_valid(self, form):
       
        deposit = form.save(commit=False)
        amount = form.cleaned_data.get('amount')
        deposit.user = self.request.user
       
        deposit.save()
        send_transaction_email(self.request.user,amount, "Deposite Message", "deposit_email.html")
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_deposit = Deposit.objects.filter(user=self.request.user).aggregate(total=models.Sum('amount'))['total'] or 0
        context['deposit_amount'] = total_deposit
        return context
    
    
