from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

from django.middleware.csrf import get_token
from django.http import HttpResponse, JsonResponse
from django.contrib import auth
from django.db.models import Q
import json

from .serializers import *
from main.models import *
from .models import *

from main.models import cakecategories

from django.http import JsonResponse

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def getAdminProducts(request):
    if request.data["params"]["role"] == "ADMIN" or  "SUPER_ADMIN":
        if str(request.user) == request.data["params"]["username"]:
            serializer = ItemSerializer(Item.objects.all(),many = True)
            return Response(serializer.data,status=status.HTTP_200_OK)
       
    return Response ('failed',status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def editAdminProduct(request):
    data = json.loads(request.body)
    item_id = data.get('id')
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')

    numberOfItems = data.get('numberOfItems')
    thumbnail = data.get('thumbnail')
    thumbnail_public_id = data.get('thumbnail_public_id')

    try:
        item = Item.objects.get(id=item_id)
        item.name = name
        item.description = description
        item.price = price
        item.numberOfItems = numberOfItems
        item.thumbnail = thumbnail
        item.thumbnail_public_id = thumbnail_public_id
        item.save()
        return JsonResponse({'message': 'Product updated successfully'}, status=200)
    except Item.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createAdminProduct(request):
    data = json.loads(request.body)
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')

    numberOfItems = data.get('numberOfItems')
    thumbnail = data.get('thumbnail')
    thumbnail_public_id = data.get('thumbnail_public_id')

    category_names = data.get('category')

    categories = CakeCategory.objects.filter(name__in=category_names)


    print(f"""
    
    
    
     category array : {category_names}
    
    
    
    """)  # Debugging line
  # Debugging line
    print(f"""
    
    
    
     category array : {categories}
    
    
    
    """)  # Debugging line
    print("Creating product with data:", data)  # Debugging line

    item = Item.objects.create(
        name=name,
        description=description,
        price=price,
        numberOfItems=numberOfItems,
        thumbnail=thumbnail,
        thumbnail_public_id=thumbnail_public_id
    )

    item.category.set(categories) 
    return JsonResponse({'message': 'Product created successfully', 'id': item.id}, status=201)