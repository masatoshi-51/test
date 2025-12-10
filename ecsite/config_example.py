"""
設定ファイルの例
このファイルを config.py にコピーして、必要に応じて設定を変更してください
"""

# HTTPリクエストのヘッダー設定
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# リクエスト間隔（秒） - サーバーに負荷をかけないように
REQUEST_DELAY = 1

# タイムアウト設定（秒）
TIMEOUT = 10

# デフォルトの最大取得商品数
DEFAULT_MAX_RESULTS = 10

# 出力ファイル名
OUTPUT_FILENAME = 'products.json'

# ==============================
# Googleスプレッドシート設定
# ==============================

# Googleサービスアカウントの秘密鍵ファイル（JSON）のパス
# 例: 'service_account.json'
SERVICE_ACCOUNT_FILE = 'service_account.json'

# データを書き込むスプレッドシート名
SHEET_NAME = 'AmazonProducts'

# データを書き込むワークシート名（シートのタブ名）
WORKSHEET_NAME = 'Sheet1'

