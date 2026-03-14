from .models import Order

def user_orders(request):
    if request.user.is_authenticated:
        # Fetch the user's orders, ordered by newest first
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        return {'user_orders': orders}
    return {'user_orders': []}
