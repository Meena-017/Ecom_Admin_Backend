from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from website.models import Products
from website.api.serialization.product_serializer import ProductSerializer

# List all products or create a new product
@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        products = Products.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Retrieve, update, or delete a product
@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id):
    try:
        product = Products.objects.get(id=id)
    except Products.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response({'success': 'Product deleted'}, status=status.HTTP_204_NO_CONTENT)
# website/api/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from website.models import AuthUser
from website.api.serialization.user_serializer import UserSerializer

# List all users or create a new user
@api_view(['GET', 'POST'])
def user_list_api(request):
    if request.method == 'GET':
        users = AuthUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, update, or delete a user
@api_view(['GET', 'PUT', 'DELETE'])
def user_detail_api(request, id):
    try:
        user = AuthUser.objects.get(id=id)
    except AuthUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response({'success': 'User deleted'}, status=status.HTTP_204_NO_CONTENT)
