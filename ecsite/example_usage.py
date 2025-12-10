"""
Amazon商品データ取得の使用例
"""

from amazon_scraper import AmazonScraper


def example_search():
    """キーワード検索の例"""
    print("=== キーワード検索の例 ===\n")
    
    # スクレイパーを作成
    scraper = AmazonScraper()
    
    # 検索キーワードを指定
    keyword = "ワイヤレスイヤホン"
    
    # 商品を検索（最大5件）
    products = scraper.search_products(keyword, max_results=5)
    
    # 結果を表示
    print(f"「{keyword}」の検索結果: {len(products)}件\n")
    for i, product in enumerate(products, 1):
        print(f"【商品 {i}】")
        print(f"  タイトル: {product.get('title', 'N/A')}")
        print(f"  価格: {product.get('price', 'N/A')}")
        print(f"  評価: {product.get('rating', 'N/A')}")
        print(f"  レビュー数: {product.get('review_count', 'N/A')}")
        print(f"  URL: {product.get('url', 'N/A')}")
        print()
    
    # JSONファイルに保存
    if products:
        scraper.save_to_json(products, f'{keyword}_products.json')
        print(f"データを {keyword}_products.json に保存しました。\n")


def example_single_product():
    """単一商品の詳細取得例"""
    print("=== 単一商品の詳細取得例 ===\n")
    
    # スクレイパーを作成
    scraper = AmazonScraper()
    
    # 商品URLを指定（実際の商品URLに置き換えてください）
    product_url = "https://www.amazon.co.jp/dp/B08N5WRWNW"  # 例のURL
    
    # 商品データを取得
    product = scraper.get_product_by_url(product_url)
    
    if product:
        print("【商品詳細】")
        print(f"  タイトル: {product.get('title', 'N/A')}")
        print(f"  価格: {product.get('price', 'N/A')}")
        print(f"  評価: {product.get('rating', 'N/A')}")
        print(f"  レビュー数: {product.get('review_count', 'N/A')}")
        print(f"  在庫状況: {product.get('availability', 'N/A')}")
        print(f"  画像URL: {product.get('image_url', 'N/A')}")
        print(f"  商品URL: {product.get('url', 'N/A')}")
        print(f"\n  説明:\n  {product.get('description', 'N/A')}")
    else:
        print("商品データの取得に失敗しました。")


def example_multiple_keywords():
    """複数のキーワードで検索する例"""
    print("=== 複数キーワード検索の例 ===\n")
    
    scraper = AmazonScraper()
    
    # 検索したいキーワードのリスト
    keywords = ["スマートフォン", "タブレット", "ノートPC"]
    
    all_products = []
    
    for keyword in keywords:
        print(f"「{keyword}」を検索中...")
        products = scraper.search_products(keyword, max_results=3)
        all_products.extend(products)
        print(f"  {len(products)}件の商品が見つかりました。\n")
    
    # すべての結果を保存
    if all_products:
        scraper.save_to_json(all_products, 'all_products.json')
        print(f"合計 {len(all_products)}件の商品データを all_products.json に保存しました。")


if __name__ == "__main__":
    # 使用例を実行
    example_search()
    print("\n" + "="*50 + "\n")
    
    # 単一商品の例（コメントアウトを外して使用）
    # example_single_product()
    # print("\n" + "="*50 + "\n")
    
    # 複数キーワードの例（コメントアウトを外して使用）
    # example_multiple_keywords()

