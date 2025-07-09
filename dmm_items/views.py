from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
import random

@api_view(['GET'])
def random_products(request):
    products = list(Product.objects.exclude(image_url_large=''))
    random.shuffle(products)
    selected = products[:10]
    data = [
        {
            "title": p.title,
            "image_url": p.image_url_large,
            "affiliate_url": p.affiliate_url,
            "rank":p.rank,
        } for p in selected
    ]
    return Response(data)

@api_view(['GET'])
def random_product(request):
    products = list(Product.objects.exclude(image_url_large=''))
    if not products:
        return Response({"error": "no product found"}, status=404)

    p = random.choice(products)

    data = {
        "title": p.title,
        "image_url": p.image_url_large,
        "affiliate_url": p.affiliate_url,
        "rank":p.rank,
    }

    return Response(data)