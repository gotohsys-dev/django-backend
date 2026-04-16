from django.core.management.base import BaseCommand
from dmm_items.models import Product
import tweepy
import random
import os

class Command(BaseCommand):
    help = 'ランダムに商品を選出してX(旧Twitter)にツイートするコマンド'

    def handle(self, *args, **options):
        # 環境変数から認証情報を取得
        API_KEY = os.getenv("X_API_KEY")
        API_SECRET = os.getenv("X_API_SECRET")
        ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
        ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")

        if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]):
            self.stderr.write(self.style.ERROR('エラー: X (Twitter) APIの認証情報が設定されていません。'))
            return

        queryset = Product.objects.exclude(image_url_large='')
        count = queryset.count()

        if count == 0:
            self.stdout.write(self.style.WARNING('ツイート対象の商品が見つかりませんでした。'))
            return

        random_index = random.randint(0, count - 1)
        product = queryset[random_index]

        # レアリティ判定 (将来的にProductモデルのプロパティにするのが理想)
        rarity = self.get_rarity(product.rank)
        
        title = product.title if product.title else "名称未設定"

        tweet_text = (
            f"【本日の運試しガチャ】\n"
            f"ランク: {product.rank}位 ({rarity})\n"
            f"{title}\n\n"
            f"{product.affiliate_url}\n"
            f"#DMM #自動ツイート"
        )

        client = tweepy.Client(
            consumer_key=API_KEY,
            consumer_secret=API_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET
        )

        try:
            response = client.create_tweet(text=tweet_text)
            self.stdout.write(self.style.SUCCESS(f'ツイート成功！ ID: {response.data["id"]}'))
        except tweepy.TweepyException as e:
            self.stderr.write(self.style.ERROR(f'ツイートに失敗しました: {e}'))

    def get_rarity(self, rank):
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