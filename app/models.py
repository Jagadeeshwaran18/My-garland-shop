from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    CATEGORY_CHOICES = [
        ('garland', 'Garland for Marriage'),
        ('marriage', 'Decoration for Marriage'),
        ('gods', 'Gods Decoration'),
        ('gods_decoration', 'Gods Garland '),
        ('others', 'Others'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='garlands/')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='garland')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def get_category_display_name(self):
        return dict(self.CATEGORY_CHOICES).get(self.category, self.category)


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'In Process'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateField(help_text="Date when the order was placed")
    delivery_date = models.DateField(help_text="Date when the order should be delivered")
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    customer_name = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=20)
    customer_email = models.EmailField()
    address = models.TextField()
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name} - {self.post.title}"
    
    def get_status_display_color(self):
        status_colors = {
            'pending': '#ffc107',    # Amber/Gold
            'processing': '#007bff', # Royal Blue
            'completed': '#28a745',  # Emerald Green
            'cancelled': '#dc3545',  # Rose Red
        }
        return status_colors.get(self.status, '#6c757d')
    
    def get_status_display_name(self):
        return dict(self.STATUS_CHOICES).get(self.status, self.status)
