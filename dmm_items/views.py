from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
import random

def get_rarity(rank):
    if rank is None:
        return "ノーマル"
    if 1 <= rank <= 100:
        return "Uレア"
    elif 101 <= rank <= 1000:
        return "Sレア"
    elif 1001 <= rank <= 3000:
        return "レア"
    else:
        return "ノーマル"

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
            "rank": p.rank,
            "rarity": get_rarity(p.rank),
        } for p in selected
    ]
    return Response(data)

@api_view(['GET'])
def random_product(request):
    products = list(Product.objects.exclude(image_url_large=''))
    if not products:
        return Response({"error": "no product found"}, status=4.04)

    p = random.choice(products)

    data = {
        "title": p.title,
        "image_url": p.image_url_large,
        "affiliate_url": p.affiliate_url,
        "rank": p.rank,
        "rarity": get_rarity(p.rank),
    }

    return Response(data)

@api_view(['GET'])
def random_videos(request):
    products = list(Product.objects.exclude(sample_movie_720=''))
    random.shuffle(products)
    selected = products[:10]
    data = [
        {
            "title": p.title,
            "video_url": p.sample_movie_720,
            "affiliate_url": p.affiliate_url,
            "rank": p.rank,
            "rarity": get_rarity(p.rank),
        } for p in selected
    ]
    return Response(data)

@api_view(['GET'])
def random_video(request):
    products = list(Product.objects.exclude(sample_movie_720=''))
    if not products:
        return Response({"error": "no video found"}, status=404)

    p = random.choice(products)

    data = {
        "title": p.title,
        "video_url": p.sample_movie_720,
        "affiliate_url": p.affiliate_url,
        "rank": p.rank,
        "rarity": get_rarity(p.rank),
    }

    return Response(data)