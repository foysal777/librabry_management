
from .models import Deposit
from django.db.models import Sum

def deposit_amount(request):
    if request.user.is_authenticated:
        total_deposit = Deposit.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0
        return {'deposit_amount': total_deposit}
    return {'deposit_amount': 0}
