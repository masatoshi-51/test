"""
Amazon商品データを取得し、Googleスプレッドシートへ反映するサンプル
"""

from amazon_scraper import AmazonScraper
from google_sheets_client import GoogleSheetsClient


def main():
    keyword = "ノートパソコン"  # 必要に応じて変更
    max_results = 10

    scraper = AmazonScraper()
    products = scraper.search_products(keyword, max_results=max_results)

    if not products:
        print("商品データが取得できませんでした。")
        return

    sheets_client = GoogleSheetsClient()
    sheets_client.sync_products(products, clear_existing=True)

    print(f"「{keyword}」のデータ {len(products)}件をスプレッドシートに反映しました。")


if __name__ == "__main__":
    main()

