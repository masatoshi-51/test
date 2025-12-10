"""
Googleスプレッドシート連携用クライアント
"""

import os
from typing import Dict, List, Optional

import gspread
from google.auth.exceptions import GoogleAuthError

try:
    import config
except ImportError:
    import config_example as config  # デフォルト設定を利用


class GoogleSheetsClient:
    """Googleスプレッドシートへ商品データを書き込むクライアント"""

    def __init__(
        self,
        service_account_file: Optional[str] = None,
        sheet_name: Optional[str] = None,
        worksheet_name: Optional[str] = None,
    ):
        self.service_account_file = service_account_file or config.SERVICE_ACCOUNT_FILE
        self.sheet_name = sheet_name or config.SHEET_NAME
        self.worksheet_name = worksheet_name or config.WORKSHEET_NAME
        self.client = None
        self.sheet = None
        self.worksheet = None

    def connect(self) -> None:
        """スプレッドシートに接続する"""
        if not os.path.exists(self.service_account_file):
            raise FileNotFoundError(
                f"サービスアカウントファイルが見つかりません: {self.service_account_file}"
            )
        try:
            self.client = gspread.service_account(filename=self.service_account_file)
            self.sheet = self.client.open(self.sheet_name)
            self.worksheet = self._get_or_create_worksheet(self.worksheet_name)
        except (gspread.SpreadsheetNotFound, GoogleAuthError) as e:
            raise RuntimeError(f"スプレッドシート接続に失敗しました: {e}") from e

    def _get_or_create_worksheet(self, name: str):
        """指定ワークシートを取得。なければ作成する。"""
        try:
            return self.sheet.worksheet(name)
        except gspread.WorksheetNotFound:
            return self.sheet.add_worksheet(title=name, rows=200, cols=20)

    def sync_products(
        self,
        products: List[Dict],
        clear_existing: bool = True,
    ) -> None:
        """
        商品データをスプレッドシートに書き込む

        Args:
            products: 商品データのリスト（辞書形式）
            clear_existing: 既存データをクリアするか
        """
        if self.worksheet is None:
            self.connect()

        if not products:
            return

        headers = self._build_headers(products)
        rows = self._build_rows(products, headers)

        if clear_existing:
            self.worksheet.clear()

        # 1行目にヘッダー、2行目以降にデータを書き込む
        self.worksheet.update([headers] + rows, value_input_option="USER_ENTERED")

    def _build_headers(self, products: List[Dict]) -> List[str]:
        """商品データに含まれるキーをヘッダーにする"""
        header_set = set()
        for product in products:
            header_set.update(product.keys())
        # 表示順を固定化（よく使う項目を先頭に）
        preferred = [
            "title",
            "price",
            "rating",
            "review_count",
            "availability",
            "image_url",
            "url",
            "description",
        ]
        # preferred順で存在するもの→その他のキーをアルファベット順で並べる
        ordered = [h for h in preferred if h in header_set]
        remaining = sorted(header_set - set(ordered))
        return ordered + remaining

    def _build_rows(self, products: List[Dict], headers: List[str]) -> List[List]:
        """商品データをヘッダー順の2次元配列に変換"""
        rows = []
        for product in products:
            row = [product.get(h, "") for h in headers]
            rows.append(row)
        return rows


def main():
    """簡単な動作確認用"""
    sample_products = [
        {
            "title": "テスト商品A",
            "price": "¥1,000",
            "rating": "4.5",
            "review_count": "120",
            "url": "https://example.com/a",
        },
        {
            "title": "テスト商品B",
            "price": "¥2,000",
            "rating": "4.0",
            "review_count": "80",
            "url": "https://example.com/b",
        },
    ]

    client = GoogleSheetsClient()
    client.sync_products(sample_products)
    print("シートへの書き込みが完了しました。")


if __name__ == "__main__":
    main()

