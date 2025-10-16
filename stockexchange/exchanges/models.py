from django.db import models
from django.contrib.auth.models import User 


class Company(models.Model):
    name = models.CharField(max_length=100, unique=True)
    initial_price = models.DecimalField(max_digits=12, decimal_places=2)
    current_price = models.DecimalField(max_digits=12, decimal_places=2)
    total_shares = models.PositiveIntegerField()
    available_shares = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="portfolios")
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    avg_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        unique_together = ('user', 'company')

    def __str__(self):
        return f"{self.user.username} - {self.company.name} ({self.quantity})"


class Order(models.Model):
    ORDER_TYPE_CHOICES = (
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    )
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('partial', 'Partially Filled'),
        ('done', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    type = models.CharField(max_length=4, choices=ORDER_TYPE_CHOICES)
    quantity = models.PositiveIntegerField()
    remaining_quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

def save(self, *args, **kwargs):
    if not self.remaining_quantity:
        self.remaining_quantity = self.quantity
    super().save(*args, **kwargs)




class Trade(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buy_trades")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sell_trades")
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company.name} | {self.quantity} @ {self.price}"
