import os
import django
import requests
import time
from datetime import datetime
from django.utils import timezone
from dotenv import load_dotenv

# Django設定
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from dmm_items.models import Product, Genre, Actress, Maker, Label, Series, Director, Author

load_dotenv()

API_ID = os.getenv("API_ID")
AFFILIATE_ID = os.getenv("AFFILIATE_ID")
BASE_URL = "https://api.dmm.com/affiliate/v3/ItemList"  # 複数フロア対応
FLOOR = "videoa"
HITS = 100

# 日付解析
def parse_date(date_str):
    if not date_str:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    return None

# dict/list 対応の name 取得
def extract_first_name(obj):
    if isinstance(obj, dict):
        return obj.get("name", "")
    elif isinstance(obj, list) and len(obj) > 0:
        return obj[0].get("name", "")
    return ""

# マスタテーブルのキャッシュ
cache = {
    "genre": {}, "actress": {}, "maker": {}, "label": {}, "series": {}, "director": {}, "author": {}
}

def get_cached_or_create(model, name, key):
    if not name:
        return None
    if name in cache[key]:
        return cache[key][name]
    obj, _ = model.objects.get_or_create(name=name)
    cache[key][name] = obj
    return obj

def fetch_dmm_data():
    existing_ids = set(Product.objects.values_list("content_id", flat=True))
    print(f"すでに保存されている件数: {len(existing_ids)}")

    params = {
        "api_id": API_ID,
        "affiliate_id": AFFILIATE_ID,
        "floor": FLOOR,
        "hits": HITS,
        "output": "json",
        "sort": "date"
    }

    offset = 1
    total = None

    while True:
        params["offset"] = offset
        response = requests.get(BASE_URL, params=params)
        data = response.json().get("result", {})

        if total is None:
            total = int(data.get("total_count", 0))
            print(f"全件数: {total}")

        items = data.get("items", [])
        if not items:
            break

        print(f"{offset}件目から {len(items)} 件取得")

        for item in items:
            cid = item.get("content_id")
            if cid in existing_ids:
                continue

            # ジャンル・女優（文字列化）
            genre_list = [g.get("name") for g in item.get("iteminfo", {}).get("genre", []) if g.get("name")]
            actress_list = [a.get("name") for a in item.get("iteminfo", {}).get("actress", []) if a.get("name")]
            genre_text = ", ".join(genre_list)
            actress_text = ", ".join(actress_list)

            # 関連テーブルにも保存（キャッシュ付き）
            for name in genre_list:
                get_cached_or_create(Genre, name, "genre")
            for name in actress_list:
                get_cached_or_create(Actress, name, "actress")

            maker_name    = extract_first_name(item.get("iteminfo", {}).get("maker"))
            label_name    = extract_first_name(item.get("iteminfo", {}).get("label"))
            series_name   = extract_first_name(item.get("iteminfo", {}).get("series"))
            director_name = extract_first_name(item.get("iteminfo", {}).get("director"))
            author_name   = extract_first_name(item.get("iteminfo", {}).get("author"))

            get_cached_or_create(Maker, maker_name, "maker")
            get_cached_or_create(Label, label_name, "label")
            get_cached_or_create(Series, series_name, "series")
            get_cached_or_create(Director, director_name, "director")
            get_cached_or_create(Author, author_name, "author")

            Product.objects.update_or_create(
                content_id=cid,
                defaults={
                    "product_id": item.get("product_id"),
                    "title": item.get("title"),
                    "volume": None,
                    "number": None,
                    "review_count": int(item.get("review", {}).get("count", 0)),
                    "review_average": float(item.get("review", {}).get("average", 0.0)),
                    "url": item.get("URL"),
                    "affiliate_url": item.get("affiliateURL"),
                    "image_url_small": item.get("imageURL", {}).get("small", ""),
                    "image_url_large": item.get("imageURL", {}).get("large", ""),
                    "sample_image_small": item.get("sampleImageURL", {}).get("small", ""),
                    "sample_image_large": item.get("sampleImageURL", {}).get("large", ""),
                    "sample_movie_476": item.get("sampleMovieURL", {}).get("size_476_306", ""),
                    "sample_movie_560": item.get("sampleMovieURL", {}).get("size_560_360", ""),
                    "sample_movie_644": item.get("sampleMovieURL", {}).get("size_644_414", ""),
                    "sample_movie_720": item.get("sampleMovieURL", {}).get("size_720_540", ""),
                    "price": item.get("prices", {}).get("price", ""),
                    "delivery_type": item.get("delivery", {}).get("type", ""),
                    "delivery_price": item.get("prices", {}).get("list_price", 0) or 0,
                    "release_date": parse_date(item.get("date")),
                    "delivery_start_date": parse_date(item.get("date_delivery")),
                    "rental_start_date": parse_date(item.get("date_rental")),
                    "is_pc": item.get("playback", {}).get("pc", True),
                    "is_smartphone": item.get("playback", {}).get("sp", True),
                    "genre": genre_text,
                    "actresses": actress_text,
                    "maker": maker_name,
                    "series": series_name,
                    "label": label_name,
                    "director": director_name,
                    "author": author_name,
                    "jancode": item.get("jancode", ""),
                    "maker_product": item.get("maker_product", ""),
                }
            )

        offset += HITS
        time.sleep(1)

if __name__ == "__main__":
    fetch_dmm_data()
