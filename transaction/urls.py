# urls.py
from django.urls import path
from .views import DepositView

urlpatterns = [
    path('deposit/', DepositView.as_view(), name='deposit'),
    # path('deposit/success/', TemplateView.as_view(template_name="deposit_success.html"), name='deposit_success'),  # Replace with your success view
]
