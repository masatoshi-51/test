"""
Amazon商品データ取得スクリプト
商品のタイトル、価格、評価、URLなどを取得します
"""

import requests
from bs4 import BeautifulSoup
import time
import json
from typing import Dict, List, Optional
import urllib.parse


class AmazonScraper:
    """Amazon商品データを取得するクラス"""
    
    def __init__(self, headers: Optional[Dict] = None):
        """
        初期化
        
        Args:
            headers: HTTPリクエストヘッダー（デフォルトのヘッダーを使用する場合はNone）
        """
        # デフォルトのヘッダーを設定（ブラウザとして認識されるように）
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def search_products(self, keyword: str, max_results: int = 10) -> List[Dict]:
        """
        キーワードで商品を検索
        
        Args:
            keyword: 検索キーワード
            max_results: 取得する最大商品数
        
        Returns:
            商品データのリスト
        """
        # 検索URLを作成
        search_url = f"https://www.amazon.co.jp/s?k={urllib.parse.quote(keyword)}"
        
        try:
            # ページを取得
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            # HTMLを解析
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 商品データを抽出
            products = []
            
            # 商品コンテナを探す（AmazonのHTML構造に基づく）
            product_elements = soup.find_all('div', {'data-component-type': 's-search-result'})
            
            for element in product_elements[:max_results]:
                product_data = self._extract_product_data(element)
                if product_data:
                    products.append(product_data)
            
            # リクエスト間隔を空ける（サーバーに負荷をかけないため）
            time.sleep(1)
            
            return products
            
        except requests.RequestException as e:
            print(f"エラーが発生しました: {e}")
            return []
    
    def get_product_by_url(self, url: str) -> Optional[Dict]:
        """
        商品URLから直接商品データを取得
        
        Args:
            url: 商品のURL
        
        Returns:
            商品データ（辞書形式）
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 商品データを抽出
            product_data = {
                'title': self._extract_title(soup),
                'price': self._extract_price(soup),
                'rating': self._extract_rating(soup),
                'review_count': self._extract_review_count(soup),
                'availability': self._extract_availability(soup),
                'description': self._extract_description(soup),
                'image_url': self._extract_image_url(soup),
                'url': url
            }
            
            time.sleep(1)
            
            return product_data
            
        except requests.RequestException as e:
            print(f"エラーが発生しました: {e}")
            return None
    
    def _extract_product_data(self, element) -> Optional[Dict]:
        """検索結果から商品データを抽出"""
        try:
            # タイトル
            title_elem = element.find('h2', class_='a-size-mini')
            if not title_elem:
                title_elem = element.find('h2', class_='a-size-base')
            title = title_elem.get_text(strip=True) if title_elem else "タイトル不明"
            
            # URL
            link_elem = element.find('a', class_='a-link-normal')
            url = "https://www.amazon.co.jp" + link_elem['href'] if link_elem and link_elem.get('href') else None
            
            # 価格
            price = self._extract_price_from_element(element)
            
            # 評価
            rating = self._extract_rating_from_element(element)
            
            # レビュー数
            review_count = self._extract_review_count_from_element(element)
            
            # 画像URL
            img_elem = element.find('img', class_='s-image')
            image_url = img_elem['src'] if img_elem and img_elem.get('src') else None
            
            return {
                'title': title,
                'price': price,
                'rating': rating,
                'review_count': review_count,
                'image_url': image_url,
                'url': url
            }
            
        except Exception as e:
            print(f"商品データの抽出中にエラー: {e}")
            return None
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """商品ページからタイトルを抽出"""
        title_elem = soup.find('span', {'id': 'productTitle'})
        if not title_elem:
            title_elem = soup.find('h1', class_='a-size-large')
        return title_elem.get_text(strip=True) if title_elem else "タイトル不明"
    
    def _extract_price(self, soup: BeautifulSoup) -> Optional[str]:
        """商品ページから価格を抽出"""
        # 複数の価格セレクタを試す
        price_selectors = [
            {'id': 'priceblock_ourprice'},
            {'id': 'priceblock_dealprice'},
            {'class': 'a-price-whole'},
            {'class': 'a-offscreen'}
        ]
        
        for selector in price_selectors:
            price_elem = soup.find('span', selector)
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                if price_text:
                    return price_text
        
        return None
    
    def _extract_price_from_element(self, element) -> Optional[str]:
        """検索結果要素から価格を抽出"""
        price_elem = element.find('span', class_='a-price-whole')
        if not price_elem:
            price_elem = element.find('span', class_='a-offscreen')
        return price_elem.get_text(strip=True) if price_elem else None
    
    def _extract_rating(self, soup: BeautifulSoup) -> Optional[str]:
        """商品ページから評価を抽出"""
        rating_elem = soup.find('span', {'id': 'acrPopover'})
        if not rating_elem:
            rating_elem = soup.find('span', class_='a-icon-alt')
        if rating_elem:
            rating_text = rating_elem.get_text(strip=True)
            # "4.5 out of 5 stars" のような形式から数値を抽出
            import re
            match = re.search(r'(\d+\.?\d*)', rating_text)
            return match.group(1) if match else None
        return None
    
    def _extract_rating_from_element(self, element) -> Optional[str]:
        """検索結果要素から評価を抽出"""
        rating_elem = element.find('span', class_='a-icon-alt')
        if rating_elem:
            rating_text = rating_elem.get_text(strip=True)
            import re
            match = re.search(r'(\d+\.?\d*)', rating_text)
            return match.group(1) if match else None
        return None
    
    def _extract_review_count(self, soup: BeautifulSoup) -> Optional[str]:
        """商品ページからレビュー数を抽出"""
        review_elem = soup.find('span', {'id': 'acrCustomerReviewText'})
        if review_elem:
            return review_elem.get_text(strip=True)
        return None
    
    def _extract_review_count_from_element(self, element) -> Optional[str]:
        """検索結果要素からレビュー数を抽出"""
        review_elem = element.find('a', class_='a-link-normal')
        if review_elem:
            review_text = review_elem.get_text(strip=True)
            return review_text
        return None
    
    def _extract_availability(self, soup: BeautifulSoup) -> Optional[str]:
        """在庫状況を抽出"""
        availability_elem = soup.find('div', {'id': 'availability'})
        if availability_elem:
            span = availability_elem.find('span')
            return span.get_text(strip=True) if span else None
        return None
    
    def _extract_description(self, soup: BeautifulSoup) -> Optional[str]:
        """商品説明を抽出"""
        desc_elem = soup.find('div', {'id': 'feature-bullets'})
        if desc_elem:
            bullets = desc_elem.find_all('span', class_='a-list-item')
            descriptions = [bullet.get_text(strip=True) for bullet in bullets if bullet.get_text(strip=True)]
            return '\n'.join(descriptions)
        return None
    
    def _extract_image_url(self, soup: BeautifulSoup) -> Optional[str]:
        """商品画像URLを抽出"""
        img_elem = soup.find('img', {'id': 'landingImage'})
        if img_elem and img_elem.get('data-old-src'):
            return img_elem['data-old-src']
        elif img_elem and img_elem.get('src'):
            return img_elem['src']
        return None
    
    def save_to_json(self, data: List[Dict], filename: str = 'products.json'):
        """
        商品データをJSONファイルに保存
        
        Args:
            data: 保存する商品データのリスト
            filename: 保存先のファイル名
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"データを {filename} に保存しました。")


def main():
    """使用例"""
    scraper = AmazonScraper()
    
    # キーワード検索の例
    print("商品を検索中...")
    keyword = "ノートパソコン"
    products = scraper.search_products(keyword, max_results=5)
    
    print(f"\n{keyword} の検索結果: {len(products)}件")
    for i, product in enumerate(products, 1):
        print(f"\n--- 商品 {i} ---")
        print(f"タイトル: {product.get('title', 'N/A')}")
        print(f"価格: {product.get('price', 'N/A')}")
        print(f"評価: {product.get('rating', 'N/A')}")
        print(f"URL: {product.get('url', 'N/A')}")
    
    # JSONファイルに保存
    if products:
        scraper.save_to_json(products, 'amazon_products.json')


if __name__ == "__main__":
    main()

