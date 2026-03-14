from django.urls import path
from . import views

urlpatterns = [
    # LOGIN/LOGOUT
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # USER
    path('', views.user_post_list, name='user_posts'),
    path('post/<int:id>/', views.post_detail, name='post_detail'),
    path('category/<str:category>/', views.category_page, name='category_page'),
    path('about/', views.about, name='about'),
    path('cart/checkout/', views.cart_checkout, name='cart_checkout'),
    path('order/<int:post_id>/', views.create_order, name='create_order'),
    
    # ADMIN
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/add/', views.add_post, name='add_post'),
    path('admin/edit/<int:id>/', views.edit_post, name='edit_post'),
    path('admin/delete/<int:id>/', views.delete_post, name='delete_post'),
    path('admin/order/<int:order_id>/update-status/', views.update_order_status, name='update_order_status'),
]
