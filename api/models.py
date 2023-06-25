from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"<< Category '{self.title}' >>"


class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    featured = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return f"<< MenuItem '{self.title}' >>"

    class Meta:
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu items"


class Cart(models.Model):
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("menuitem", "user")

    def __str__(self):
        return f"<< Cart '{self.user.pk}' >>"


class Order(models.Model):
    status = models.BooleanField(default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="delivery_crew", null=True)
    
    def __str__(self):
        return f"<< Order {self.user.id} {self.pk} >>"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"<< Order {self.order} >>"

    class Meta:
        unique_together = ('order', 'menuitem')