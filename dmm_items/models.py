# マイグレーション作成	python manage.py makemigrations
# マイグレーション適用	python manage.py migrate
# python manage.py runserver

from django.db import models

class Genre(models.Model):
    genre_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Series(models.Model):
    name = models.CharField(max_length=255, unique=True)
    series_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name
class Maker(models.Model):
    maker_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
class Actress(models.Model):
    actress_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Director(models.Model):
    director_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Author(models.Model):
    author_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Label(models.Model):
    label_id = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

from django.db import models

class Product(models.Model):
    # 基本情報
    service_code = models.CharField(max_length=30,null=True, blank=True)            # digital など
    service_name = models.CharField(max_length=30,null=True, blank=True)            # 動画、書籍など
    floor_code = models.CharField(max_length=30,null=True, blank=True)              # videoa など
    floor_name = models.CharField(max_length=30,null=True, blank=True)              # ビデオ、同人など
    category_name = models.CharField(max_length=50,null=True, blank=True)          # ビデオ (動画)、など

    content_id = models.CharField(max_length=30, unique=True) # 商品ID（例: 15dss00145）
    product_id = models.CharField(max_length=30)              # 品番（例: 15dss00145dl）
    title = models.CharField(max_length=200)

    volume = models.IntegerField(null=True, blank=True)       # 収録時間（分）
    number = models.IntegerField(null=True, blank=True)       # 巻数

    rank = models.IntegerField(null=True, blank=True)         # ランキング

    # レビュー
    review_count = models.IntegerField(default=0)
    review_average = models.FloatField(default=0.0)

    # 商品ページ・アフィリエイト
    url = models.URLField()
    affiliate_url = models.URLField()

    # 画像URL
    image_url_list = models.URLField(null=True, blank=True)   # imageURL.list（リストページ用）
    image_url_small = models.URLField(null=True, blank=True)  # imageURL.small
    image_url_large = models.URLField(null=True, blank=True)  # imageURL.large

    # サンプル画像
    sample_image_small = models.URLField(null=True, blank=True)  # sampleImageURL.sample_s.image
    sample_image_large = models.URLField(null=True, blank=True)  # sampleImageURL.sample_l.image

    # サンプル動画
    sample_movie_476 = models.URLField(null=True, blank=True)    # sampleMovieURL.size_476_306
    sample_movie_560 = models.URLField(null=True, blank=True)    # sampleMovieURL.size_560_360
    sample_movie_644 = models.URLField(null=True, blank=True)    # sampleMovieURL.size_644_414
    sample_movie_720 = models.URLField(null=True, blank=True)    # sampleMovieURL.size_720_480

    # 立ち読みページ
    tachiyomi_url = models.URLField(null=True, blank=True)       # tachiyomi.URL
    tachiyomi_affiliate_url = models.URLField(null=True, blank=True) # tachiyomi.affiliateURL

    # 価格・配信
    price = models.CharField(max_length=20)                  # prices.price（例: 300〜）
    delivery_type = models.CharField(max_length=20)          # delivery.type
    delivery_price = models.IntegerField(null=True, blank=True) # delivery.price

    # 対応端末
    is_pc = models.BooleanField(default=True)                # pc_flag（1→True）
    is_smartphone = models.BooleanField(default=True)        # sp_flag（1→True）

    # 日付・コード類
    release_date = models.DateTimeField(null=True, blank=True)   # date（例: 2012/08/03 10:00）
    jancode = models.CharField(max_length=13, null=True, blank=True)
    maker_product = models.CharField(max_length=50, null=True, blank=True)

    # 関連情報（別モデルと接続）
    genre = models.TextField(null=True, blank=True)
    actresses = models.TextField(null=True, blank=True)
    # genres = models.ManyToManyField(Genre, blank=True)
    # actresses = models.ManyToManyField(Actress, blank=True)
    maker = models.CharField(max_length=50, null=True, blank=True)
    series = models.CharField(max_length=50, null=True, blank=True)
    label = models.CharField(max_length=100, null=True, blank=True)
    director = models.CharField(max_length=100, null=True, blank=True)
    author = models.CharField(max_length=200, null=True, blank=True)

    #キャンペーン情報
    campaign_date_begin = models.DateTimeField(null=True, blank=True)
    campaign_date_end = models.DateTimeField(null=True, blank=True)
    campaign_title = models.CharField(max_length=100, null=True, blank=True)

    # 管理用
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
