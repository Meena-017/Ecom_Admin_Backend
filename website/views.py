from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Products, AuthUser
from django.db.models import Sum

# -------------------- Login / Logout / Signup --------------------
def login_page(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get("next") or "dashboard")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, "website/login.html")


def logout_page(request):
    logout(request)
    return redirect("login")


def signup_page(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if AuthUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        elif AuthUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
        else:
            AuthUser.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Account created successfully. Please login.")
            return redirect("login")

    return render(request, "website/signup.html")


# -------------------- Dashboard --------------------
@login_required(login_url="login")
def dashboard_page(request):
    total_products = Products.objects.count()
    total_users = AuthUser.objects.count()
    total_stock = Products.objects.aggregate(Sum("stock"))["stock__sum"] or 0
    most_expensive = Products.objects.order_by("-price").first()

    return render(request, "website/dashboard.html", {
        "total_products": total_products,
        "total_users": total_users,
        "total_stock": total_stock,
        "most_expensive": most_expensive,
    })


# -------------------- Product List --------------------
@login_required(login_url="login")
def product_list_page(request):
    products = Products.objects.all()

    if request.method == "POST":
        if "add_product" in request.POST:
            Products.objects.create(
                name=request.POST.get("name"),
                description=request.POST.get("description"),
                price=request.POST.get("price"),
                stock=request.POST.get("stock"),
            )
            messages.success(request, "Product added successfully!")
            return redirect("frontend_product_list")  # ✅ updated URL name

        if "edit_product" in request.POST:
            product = get_object_or_404(Products, id=request.POST.get("product_id"))
            product.name = request.POST.get("name")
            product.description = request.POST.get("description")
            product.price = request.POST.get("price")
            product.stock = request.POST.get("stock")
            product.save()
            messages.success(request, "Product updated successfully!")
            return redirect("frontend_product_list")  # ✅ updated URL name

        if "delete_product" in request.POST:
            product = get_object_or_404(Products, id=request.POST.get("product_id"))
            product.delete()
            messages.success(request, "Product deleted successfully!")
            return redirect("frontend_product_list")  # ✅ updated URL name

    return render(request, "website/product_list.html", {"products": products})


# -------------------- Cart --------------------
def _get_cart_session(request):
    return request.session.setdefault("cart", {})


@login_required(login_url="login")
def add_to_cart(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    cart = _get_cart_session(request)
    str_id = str(product_id)

    # Store cart as dict with quantity
    if str_id in cart:
        cart[str_id] += 1
    else:
        cart[str_id] = 1

    request.session.modified = True
    messages.success(request, f"Added '{product.name}' to cart.")
    return redirect("frontend_product_list")  # ✅ updated URL name


@login_required(login_url="login")
def remove_from_cart(request, product_id):
    cart = _get_cart_session(request)
    str_id = str(product_id)
    if str_id in cart:
        del cart[str_id]
        request.session.modified = True
        messages.success(request, "Item removed from cart.")
    return redirect("cart")  # remains same


@login_required(login_url="login")
def cart_page(request):
    cart = request.session.get("cart", {})
    items, total = [], 0

    for pid_str, qty in cart.items():
        try:
            product = Products.objects.get(id=int(pid_str))
            subtotal = float(product.price) * int(qty)
            items.append({"product": product, "quantity": qty, "subtotal": subtotal})
            total += subtotal
        except Products.DoesNotExist:
            continue

    return render(request, "website/cart.html", {"items": items, "total": total})


# -------------------- User List --------------------
@login_required(login_url="login")
def user_list_page(request):
    users = AuthUser.objects.all()

    if request.method == "POST":
        if "add_user" in request.POST:
            AuthUser.objects.create_user(
                username=request.POST.get("username"),
                email=request.POST.get("email"),
                password=request.POST.get("password"),
                is_superuser=True if request.POST.get("is_superuser") == "on" else False,
            )
            messages.success(request, "User added successfully!")
            return redirect("user_list")

        if "edit_user" in request.POST:
            user = get_object_or_404(AuthUser, id=request.POST.get("user_id"))
            user.username = request.POST.get("username")
            user.email = request.POST.get("email")
            if request.POST.get("password"):
                user.set_password(request.POST.get("password"))
            user.is_superuser = True if request.POST.get("is_superuser") == "on" else False
            user.save()
            messages.success(request, "User updated successfully!")
            return redirect("user_list")

        if "delete_user" in request.POST:
            user = get_object_or_404(AuthUser, id=request.POST.get("user_id"))
            user.delete()
            messages.success(request, "User deleted successfully!")
            return redirect("user_list")

    return render(request, "website/user_list.html", {"users": users})
