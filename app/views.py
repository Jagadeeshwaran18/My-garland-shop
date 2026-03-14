from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
import json
from .models import Post, Order

# Create your views here.


# LOGIN
def login_view(request):
    # If user is already logged in, redirect them
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        return redirect('user_posts')
    
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(
                username=username,
                password=password
            )

            if user:
                login(request, user)
                # Automatically detect if user is admin (staff) or regular user
                # Admin (staff) → Admin Dashboard
                # Regular user → Home Page
                if user.is_staff:
                    return redirect('admin_dashboard')
                else:
                    return redirect('user_posts')
            else:
                error_message = "Invalid username or password. Please try again."
        else:
            error_message = "Please enter both username and password."

    return render(request, 'auth/login.html', {'error_message': error_message})


def register_view(request):
    # Redirect logged-in users away from register
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        return redirect('user_posts')

    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not username or not password or not confirm_password:
            error_message = "Please fill out all required fields."
        elif password != confirm_password:
            error_message = "Passwords do not match."
        else:
            try:
                User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                messages.success(request, "Account created successfully! You can now log in.")
                return redirect('login')
            except IntegrityError:
                error_message = "Username already exists. Please choose another."
            except Exception:
                error_message = "Unable to create account. Please try again."

    return render(request, 'auth/register.html', {'error_message': error_message})


def logout_view(request):
    logout(request)
    return redirect('login')


# USER VIEWS (require login)
# Public view (no login required for browsing)
def user_post_list(request):
    posts = Post.objects.all()
    categories = Post.CATEGORY_CHOICES
    
    return render(request, 'user_page/index.html', {
        'posts': posts,
        'categories': categories,
    })

@login_required(login_url='login')
def category_page(request, category):
    # Get posts for the selected category
    posts = Post.objects.filter(category=category)
    
    # Get category display name
    category_choices = dict(Post.CATEGORY_CHOICES)
    category_name = category_choices.get(category, category)
    
    # Get all categories for navigation
    categories = Post.CATEGORY_CHOICES
    
    return render(request, 'user_page/category_page.html', {
        'posts': posts,
        'category': category,
        'category_name': category_name,
        'categories': categories,
    })

@login_required(login_url='login')
def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'user_page/post_detail.html', {'post': post})

# Public view
def about(request):
    return render(request, 'user_page/about.html')


# ORDER VIEWS
@login_required(login_url='login')
def cart_checkout(request):
    if request.method == 'POST':
        try:
            cart_data_json = request.POST.get('cart_data')
            if not cart_data_json:
                messages.error(request, 'Your cart is empty.')
                return redirect('user_posts')
                
            cart_items = json.loads(cart_data_json)
            
            delivery_date = request.POST.get('delivery_date')
            customer_name = request.POST.get('customer_name')
            customer_phone = request.POST.get('customer_phone')
            customer_email = request.POST.get('customer_email')
            address = request.POST.get('address')
            notes = request.POST.get('notes', '')
            
            if not all([delivery_date, customer_name, customer_phone, customer_email, address]):
                messages.error(request, 'Please fill in all required fields.')
                return render(request, 'user_page/cart_checkout.html')
            
            order_date = timezone.now().date()
            delivery_date_obj = datetime.strptime(delivery_date, '%Y-%m-%d').date()
            
            # Create an order for each item in the cart array
            for item in cart_items:
                post = get_object_or_404(Post, id=item.get('id'))
                Order.objects.create(
                    user=request.user,
                    post=post,
                    order_date=order_date,
                    delivery_date=delivery_date_obj,
                    quantity=1,
                    total_price=post.price,
                    customer_name=customer_name,
                    customer_phone=customer_phone,
                    customer_email=customer_email,
                    address=address,
                    notes=notes,
                    status='pending'
                )
                
            messages.success(request, 'All cart items ordered successfully!')
            return render(request, 'user_page/order_success.html')
            
        except Exception as e:
            messages.error(request, f'Error creating orders: {str(e)}')
            
    return render(request, 'user_page/cart_checkout.html')

@login_required(login_url='login')
def create_order(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        try:
            delivery_date = request.POST.get('delivery_date')
            quantity = int(request.POST.get('quantity', 1))
            customer_name = request.POST.get('customer_name')
            customer_phone = request.POST.get('customer_phone')
            customer_email = request.POST.get('customer_email')
            address = request.POST.get('address')
            notes = request.POST.get('notes', '')
            
            if not all([delivery_date, customer_name, customer_phone, customer_email, address]):
                messages.error(request, 'Please fill in all required fields.')
                return render(request, 'user_page/create_order.html', {'post': post})
            
            total_price = post.price * quantity
            order_date = timezone.now().date()
            
            Order.objects.create(
                user=request.user,
                post=post,
                order_date=order_date,
                delivery_date=datetime.strptime(delivery_date, '%Y-%m-%d').date(),
                quantity=quantity,
                total_price=total_price,
                customer_name=customer_name,
                customer_phone=customer_phone,
                customer_email=customer_email,
                address=address,
                notes=notes,
                status='pending'
            )
            messages.success(request, 'Order placed successfully!')
            return redirect('user_posts')
        except Exception as e:
            messages.error(request, f'Error creating order: {str(e)}')
    
    return render(request, 'user_page/create_order.html', {'post': post})


# ADMIN VIEWS
@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('login')

    posts = Post.objects.all()
    orders = Order.objects.all().order_by('-created_at')
    # Get all users who have logged in (have last_login)
    all_users = User.objects.filter(last_login__isnull=False).order_by('-last_login')
    
    return render(request, 'admin_page/dashboard.html', {
        'posts': posts,
        'orders': orders,
        'all_users': all_users,
        'users_count': all_users.count(),
        'order_status_choices': Order.STATUS_CHOICES,
    })


@login_required
def update_order_status(request, order_id):
    if not request.user.is_staff:
        return redirect('login')
    
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES).keys():
            order.status = new_status
            order.save()
            messages.success(request, f'Order status updated to {order.get_status_display()}')
    
    return redirect('admin_dashboard')


@login_required
def add_post(request):
    if not request.user.is_staff:
        return redirect('login')

    if request.method == 'POST':
        try:
            Post.objects.create(
                title=request.POST.get('title', ''),
                description=request.POST.get('description', ''),
                category=request.POST.get('category', 'garland'),
                price=request.POST.get('price', 0),
                image=request.FILES.get('image')
            )
            messages.success(request, 'Post created successfully!')
            return redirect('admin_dashboard')
        except Exception as e:
            return render(request, 'admin_page/add_post.html', {'error_message': f'Error creating post: {str(e)}'})

    return render(request, 'admin_page/add_post.html', {
        'categories': Post.CATEGORY_CHOICES
    })


@login_required
def edit_post(request, id):
    if not request.user.is_staff:
        return redirect('login')
    
    post = get_object_or_404(Post, id=id)

    if request.method == 'POST':
        try:
            post.title = request.POST.get('title', post.title)
            post.description = request.POST.get('description', post.description)
            post.category = request.POST.get('category', post.category)
            post.price = request.POST.get('price', post.price)
            if 'image' in request.FILES:
                post.image = request.FILES['image']
            post.save()
            return redirect('admin_dashboard')
        except Exception as e:
            return render(request, 'admin_page/edit_post.html', {'post': post, 'error_message': f'Error updating post: {str(e)}'})

    return render(request, 'admin_page/edit_post.html', {'post': post})


@login_required
def delete_post(request, id):
    if not request.user.is_staff:
        return redirect('login')
    
    post = get_object_or_404(Post, id=id)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('admin_dashboard')
    
    return render(request, 'admin_page/delete_post.html', {'post': post})
