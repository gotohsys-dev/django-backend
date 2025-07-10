
import os
import django
import math

# Djangoプロジェクトの設定を読み込む
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection
from dmm_items.models import Product

def cleanup_products():
    """
    Productテーブルの後半のデータを削除し、DBファイルを最適化する
    """
    try:
        # 1. 総件数を取得
        total_count = Product.objects.count()
        if total_count == 0:
            print("Productテーブルにデータがありません。")
            return

        print(f"現在のProduct数: {total_count}")

        # 2. 削除する件数を計算（総数の半分）
        limit = math.ceil(total_count / 2)
        print(f"削除する件数: {limit}")

        # 3. 削除対象のIDを降順で取得
        products_to_delete_ids = Product.objects.order_by('-id').values_list('id', flat=True)[:limit]
        
        if not products_to_delete_ids:
            print("削除対象のデータが見つかりませんでした。")
            return

        # 4. データを一括削除
        deleted_count, _ = Product.objects.filter(id__in=list(products_to_delete_ids)).delete()
        print(f"{deleted_count}件のProductを削除しました。")

        # 5. VACUUMを実行してDBファイルを最適化
        print("データベースを最適化しています（VACUUM）...")
        with connection.cursor() as cursor:
            cursor.execute("VACUUM;")
        print("最適化が完了しました。")

    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    cleanup_products()
