import requests
from time import sleep
from urllib.parse import urlencode

# Djangoと連携する場合（manage.py外から実行するなら）
import os
import django

from dotenv import load_dotenv
from django.utils import timezone
from datetime import datetime
    
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # プロジェクト名に合わせる
django.setup()

from dmm_items.models import Product, Genre, Actress, Series, Maker, Label, Director, Author

Product.objects.all().delete() # 全データ削除

# --- API基本情報 ---
load_dotenv()
API_URL = "https://api.dmm.com/affiliate/v3/ItemList"
API_ID = os.getenv("DMM_API_ID")
AFFILIATE_ID = os.getenv("DMM_AFFILIATE_ID")

# --- パラメータ設定 ---
params = {
    "api_id": API_ID,
    "affiliate_id": AFFILIATE_ID,
    "site": "FANZA",            # または DMM.R18
    "service": "digital",         # 動画: video / 電子書籍: book / 通販: mono など
    "hits": 100,                  # 1回の取得件数（最大100）
    "sort": "rank",               # ランキング順
    "offset": 1,                  # 最初の位置
    "output": "json",
    # "keyword": "倉多",        # 任意（キーワードで絞る）
}

def parse_date(date_str):
    if not date_str:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(date_str, fmt)
            return timezone.make_aware(dt)  # ← ここを追加
        except ValueError:
            continue
    print(f"Unrecognized date format: {date_str}")
    return None

def parse_price(value):
    if value in [None, "", "-", "－"]:
        return 0
    try:
        return int(str(value).replace(",", "").strip())
    except (ValueError, TypeError):
        return 0

def parse_volume(value):
    if not value:
        return None
    try:
        return int("".join(filter(str.isdigit, value)))
    except ValueError:
        return None

def extract_first_name(obj):
    """
    makerやlabelなどがdictまたはlistのどちらでも対応できるようにする
    """
    if isinstance(obj, dict):
        return obj.get("name", "")
    elif isinstance(obj, list) and len(obj) > 0:
        return obj[0].get("name", "")
    return ""

def fetch_dmm_data():
    total_results = None
    all_fetched = 0

    # すでに登録されている商品の数を取得してoffsetに設定
    offset = Product.objects.count() + 1
    print(f"すでに保存されている件数: {offset - 1}")
    print(f"{offset}件目から取得を開始します。")

    while True:
        params["offset"] = offset
        query = urlencode(params)
        url = f"{API_URL}?{query}"

        response = requests.get(url)
        if response.status_code != 200:
            print(f"APIエラー: {response.status_code}")
            break

        data = response.json()
        result = data.get("result", {})
        items = result.get("items", [])

        if not total_results:
            total_results = int(result.get("total_count", 0))
            print(f"全件数: {total_results}")

        if not items:
            print("これ以上アイテムがありません。終了。")
            break

        for item in items:
            product_id = item.get("product_id")
            affiliate_url = item.get("affiliateURL")

            if not product_id or not affiliate_url:
                print("product_id または affiliate_url がないためスキップ")
                continue
            
            # genre
            genre_list = [g.get("name") for g in item.get("iteminfo", {}).get("genre", []) if g.get("name")]
            genre_text = ", ".join(genre_list)

            # actresses
            actress_list = [a.get("name") for a in item.get("iteminfo", {}).get("actress", []) if a.get("name")]
            actress_text = ", ".join(actress_list)

            series_name = extract_first_name(item.get("iteminfo", {}).get("series"))
            label_name = extract_first_name(item.get("iteminfo", {}).get("label"))
            maker_name = extract_first_name(item.get("iteminfo", {}).get("maker"))
            director_name = extract_first_name(item.get("iteminfo", {}).get("director"))
            author_name = extract_first_name(item.get("iteminfo", {}).get("author")) 
            campaigns = item.get("campaign", [])
            campaign = campaigns[0] if isinstance(campaigns, list) and campaigns else {}     
            
            product, created = Product.objects.update_or_create(
                content_id=item.get("content_id"),
                defaults={
                    "rank": offset,
                    "product_id": item.get("product_id"),
                    "title": item.get("title"),
                    "volume": parse_volume(item.get("volume")),
                    "number": item.get("number", None),

                    "service_code": item.get("service_code", ""),
                    "service_name": item.get("service_name", ""),
                    "floor_code": item.get("floor_code", ""),
                    "floor_name": item.get("floor_name", ""),
                    "category_name": item.get("category_name", ""),

                    "review_count": item.get("review", {}).get("count") or 0,
                    "review_average": item.get("review", {}).get("average") or 0.0,

                    "url": item.get("URL"),
                    "affiliate_url": item.get("affiliateURL"),
                    "image_url_list": item.get("imageURL", {}).get("list", ""),
                    "image_url_small": item.get("imageURL", {}).get("small", ""),
                    "image_url_large": item.get("imageURL", {}).get("large", ""),
                    "tachiyomi_url": item.get("tachiyomi", {}).get("URL", ""),
                    "tachiyomi_affiliate_url": item.get("tachiyomi", {}).get("affiliateURL", ""),
                    "sample_image_small": item.get("sampleImageURL", {}).get("sample_s", {}).get("image", ""),
                    "sample_image_large": item.get("sampleImageURL", {}).get("sample_l", {}).get("image", ""),
                    "sample_movie_476": item.get("sampleMovieURL", {}).get("size_476_306", ""),
                    "sample_movie_560": item.get("sampleMovieURL", {}).get("size_560_360", ""),
                    "sample_movie_644": item.get("sampleMovieURL", {}).get("size_644_414", ""),
                    "sample_movie_720": item.get("sampleMovieURL", {}).get("size_720_480", ""),
                    "price": item.get("prices", {}).get("price", ""),
                    "delivery_type": item.get("delivery", {}).get("type", ""),
                    "delivery_price": parse_price(item.get("delivery", {}).get("price", 0)),
                    "release_date": parse_date(item.get("date")),
                    "is_pc": item.get("playback", {}).get("pc") == 1,
                    "is_smartphone": item.get("playback", {}).get("sp") == 1,
                    "jancode": item.get("jancode") or "",
                    "maker_product": item.get("maker_product") or "",
                    "genre": genre_text,
                    "actresses": actress_text,
                    "maker": maker_name,
                    "series": series_name,
                    "label": label_name,
                    "director": director_name,
                    "author": author_name,
                    "campaign_date_begin": parse_date(campaign.get("date_begin", "")),
                    "campaign_date_end": parse_date(campaign.get("date_end", "")),
                    "campaign_title": campaign.get("title", "")
                }
            )

        # 女優とジャンルの処理
        actress_names = []
        for actress_info in item.get("iteminfo", {}).get("actress", []):
            name = actress_info.get("name")
            if name:
                actress_names.append(name)
                Actress.objects.get_or_create(name=name)

        genre_names = []
        for genre_info in item.get("iteminfo", {}).get("genre", []):
            name = genre_info.get("name")
            if name:
                genre_names.append(name)
                Genre.objects.get_or_create(name=name)

        # Series（シリーズ）
        if series_name:
            Series.objects.get_or_create(name=series_name)
            product.series_text = series_name

        # Maker（メーカー）
        if maker_name:
            Maker.objects.get_or_create(name=maker_name)
            product.maker_text = maker_name

        # Label（レーベル）
        if label_name:
            Label.objects.get_or_create(name=label_name)
            product.label_text = label_name

        # Director（監督）
        if director_name:
            Director.objects.get_or_create(name=director_name)
            product.director_text = director_name

        # Author（原作）
        if author_name:
            Author.objects.get_or_create(name=author_name)
            product.author_text = author_name

        # Productモデルに文字列で保存（最後にまとめて）
        product.actresses_text = ", ".join(actress_names)
        product.genres_text = ", ".join(genre_names)
        product.save()

        print(f"{offset}件目から {len(items)} 件取得")
        all_fetched += len(items)
        offset += len(items)

        if all_fetched + (offset - 1) >= total_results:
            print("全件取得完了")
            break

        sleep(1)  # APIへの過剰アクセスを防ぐためのウェイト

if __name__ == "__main__":
    fetch_dmm_data()
