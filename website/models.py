# website/models.py
import django.db.models as model
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# -------------------- Product Models --------------------
class Products(model.Model):
    name = model.CharField(max_length=250)
    description = model.TextField()
    price = model.DecimalField(max_digits=19, decimal_places=2)
    stock = model.IntegerField(default=0)

    def __str__(self):
        return self.name

class ProductImage(model.Model):
    product = model.ForeignKey(Products, on_delete=model.CASCADE, related_name='images')
    image = model.ImageField(upload_to='product_images/')

    def __str__(self):
        return f"{self.product.name} Image"


# -------------------- Custom Auth User --------------------
class AuthUser(AbstractUser):
    email = model.EmailField(unique=True)
    # username is already present in AbstractUser
    # Remove unnecessary fields to avoid confusion
    first_name = None
    last_name = None
    user_permissions = None
    groups = None

    def __str__(self):
        return self.username


# -------------------- Signals --------------------
@receiver(post_save, sender=AuthUser)
def create_auth_user_token(sender, instance, created, **kwargs):
    if created:
        from rest_framework.authtoken.models import Token
        Token.objects.create(user=instance)
