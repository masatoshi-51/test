# Amazon商品データ取得ガイド 📦

このガイドでは、Amazonから商品データを取得する方法を、小学生でも分かるように説明します！

## 📚 目次

1. [これは何をするもの？](#これは何をするもの)
2. [必要な準備](#必要な準備)
3. [インストール手順](#インストール手順)
4. [使い方](#使い方)
5. [トラブルシューティング](#トラブルシューティング)

---

## これは何をするもの？

このプログラムは、Amazonのウェブサイトから商品の情報を自動的に取得するツールです。

**取得できる情報：**
- 📝 商品のタイトル（名前）
- 💰 価格
- ⭐ 評価（星の数）
- 💬 レビューの数
- 🖼️ 商品の画像
- 🔗 商品のURL（リンク）

**例えば：**
- 「ノートパソコン」と検索すると、ノートパソコンの商品情報が自動で集まります
- 商品のURLを指定すると、その商品の詳しい情報が取得できます

---

## 必要な準備

### 1. Pythonがインストールされているか確認

**Windowsの場合：**
1. スタートメニューを開く
2. 「cmd」と入力してEnterキーを押す
3. 黒い画面（コマンドプロンプト）が開く
4. 次のコマンドを入力してEnterキーを押す：
   ```
   python --version
   ```
5. 「Python 3.x.x」のように表示されればOK！
   - もし「'python' は、内部コマンドまたは外部コマンド...」と表示されたら、Pythonをインストールする必要があります

**Pythonのインストール方法：**
- [Python公式サイト](https://www.python.org/downloads/)からダウンロード
- インストール時に「Add Python to PATH」にチェックを入れることを忘れずに！

### 2. 必要なファイルを確認

ECsiteフォルダに以下のファイルがあることを確認してください：
- ✅ `amazon_scraper.py` - メインプログラム
- ✅ `requirements.txt` - 必要なライブラリのリスト
- ✅ `example_usage.py` - 使用例
- ✅ `README.md` - このファイル

---

## インストール手順

### ステップ1: フォルダに移動する

1. コマンドプロンプト（黒い画面）を開く
2. 次のコマンドでECsiteフォルダに移動します：
   ```
   cd 実践\ECsite
   ```
   （フォルダの場所が違う場合は、正しいパスを入力してください）

### ステップ2: 必要なライブラリをインストール

次のコマンドを入力してEnterキーを押します：
```
pip install -r requirements.txt
```

**何が起こるか：**
- プログラムが動くために必要な「部品」（ライブラリ）が自動でダウンロードされます
- 少し時間がかかることがあります
- 「Successfully installed...」と表示されれば完了です！

**もしエラーが出たら：**
- `pip` が見つからない場合は、`python -m pip install -r requirements.txt` を試してください

---

## 使い方

### 方法1: キーワードで商品を検索する 🔍

**ステップ1:** プログラムを実行する

コマンドプロンプトで次のコマンドを入力：
```
python example_usage.py
```

**ステップ2:** 結果を確認する

- 画面に商品情報が表示されます
- `ワイヤレスイヤホン_products.json` というファイルが作成されます
- このファイルをメモ帳で開くと、商品データがJSON形式で保存されています

**ステップ3:** 自分のキーワードで検索する

`example_usage.py` ファイルを開いて、次の行を変更します：
```python
keyword = "ワイヤレスイヤホン"  # ← ここを変更！
```

例えば：
```python
keyword = "ゲーミングマウス"
keyword = "キーボード"
keyword = "モニター"
```

### 方法2: プログラムを直接使う 💻

**ステップ1:** Pythonの対話モードで使う

コマンドプロンプトで：
```
python
```

**ステップ2:** プログラムを読み込む

```python
from amazon_scraper import AmazonScraper

# スクレイパーを作成
scraper = AmazonScraper()

# 商品を検索（例：ノートパソコン）
products = scraper.search_products("ノートパソコン", max_results=5)

# 結果を表示
for product in products:
    print(f"タイトル: {product['title']}")
    print(f"価格: {product['price']}")
    print("---")
```

**ステップ3:** 結果をファイルに保存

```python
scraper.save_to_json(products, 'my_products.json')
```

### 方法3: 商品URLから直接取得する 🔗

特定の商品のURLがある場合：

```python
from amazon_scraper import AmazonScraper

scraper = AmazonScraper()

# 商品URLを指定
url = "https://www.amazon.co.jp/dp/B08N5WRWNW"  # ← 実際のURLに変更

# 商品データを取得
product = scraper.get_product_by_url(url)

# 結果を表示
print(f"タイトル: {product['title']}")
print(f"価格: {product['price']}")
print(f"評価: {product['rating']}")
```

---

## トラブルシューティング

### 問題1: 「ModuleNotFoundError」というエラーが出る

**原因：** 必要なライブラリがインストールされていません

**解決方法：**
```
pip install requests beautifulsoup4 lxml
```

### 問題2: 商品データが取得できない

**原因：** AmazonのHTML構造が変わった可能性があります

**解決方法：**
- 時間をおいて再度試す
- 別のキーワードで試す
- インターネット接続を確認する

### 問題3: 「403 Forbidden」エラーが出る

**原因：** Amazonが自動アクセスをブロックしている可能性があります

**解決方法：**
- リクエスト間隔を長くする（`time.sleep(2)` など）
- User-Agentを更新する
- VPNを使用する（推奨されない場合もあります）

### 問題4: 価格が取得できない

**原因：** 商品によって価格の表示方法が異なります

**解決方法：**
- 商品ページのURLから直接取得を試す
- 別の商品で試す

---

## ⚠️ 重要な注意事項

1. **利用規約を守る**
   - Amazonの利用規約を確認してください
   - 過度なアクセスは避けましょう
   - 商用利用の場合は、Amazon Product Advertising APIの使用を検討してください

2. **リクエスト間隔**
   - プログラムには自動で1秒の待機時間が設定されています
   - サーバーに負荷をかけないようにしましょう

3. **データの使用**
   - 取得したデータは個人利用の範囲で使用してください
   - 商用利用の場合は適切な許可を取得してください

---

## 📖 もっと詳しく知りたい方へ

### カスタマイズのヒント

1. **取得する商品数を変更**
   ```python
   products = scraper.search_products("キーワード", max_results=20)  # 20件取得
   ```

2. **複数のキーワードで検索**
   ```python
   keywords = ["キーワード1", "キーワード2", "キーワード3"]
   for keyword in keywords:
       products = scraper.search_products(keyword)
       # 処理...
   ```

3. **結果をフィルタリング**
   ```python
   # 価格が含まれる商品だけを抽出
   products_with_price = [p for p in products if p.get('price')]
   ```

### 次のステップ

- CSV形式で保存する機能を追加
- 価格の変動を追跡する機能を追加
- 他のECサイト（楽天、Yahooショッピングなど）にも対応

---

## 🎉 おめでとうございます！

これで、Amazonから商品データを取得できるようになりました！

質問や問題がある場合は、エラーメッセージを確認して、上記のトラブルシューティングを参考にしてください。

**楽しいプログラミングを！** 🚀

---

## 🗂️ Googleスプレッドシートに反映する方法

### 1. ざっくり流れ
1. Googleのサービスアカウントを作る（無料）
2. 秘密鍵のJSONファイルをダウンロードする
3. スプレッドシートを作り、サービスアカウントのメールを共有設定で「編集者」に追加
4. `sync_to_sheets.py` を動かすと、商品データがシートに書き込まれる

### 2. 準備（10分くらい）
1. [Google Cloud Console](https://console.cloud.google.com/) にアクセスしてログイン
2. 新しいプロジェクトを作成（名前は何でもOK）
3. 左上メニュー → 「APIとサービス」 → 「APIライブラリ」を開く
4. 「Google Sheets API」を検索して「有効にする」をクリック
5. 左の「認証情報」 → 「認証情報を作成」 → 「サービスアカウント」
6. 名前を入れて「作成」→ 権限はスキップしてOK → 「完了」
7. できたサービスアカウントをクリック → 「鍵」タブ → 「鍵を追加」→「新しい鍵を作成」→ JSON を選んでダウンロード
8. ダウンロードしたJSONファイルを `service_account.json` にリネームし、`ECsite` フォルダに置く  
   （ファイル名を変えたい場合は `config.py` の `SERVICE_ACCOUNT_FILE` を同じ名前に変更）

### 3. スプレッドシート側の設定（3分）
1. Googleスプレッドシートを新規作成（名前例：`AmazonProducts`）
2. 右上「共有」から、サービスアカウントのメールアドレス（`xxx@xxx.iam.gserviceaccount.com`）を「編集者」で追加
3. シートのタブ名（下の名前）が `Sheet1` であることを確認  
   （違う場合は `config.py` の `WORKSHEET_NAME` を同じ名前に変更）

### 4. 設定ファイルを確認（1分）
`config_example.py` をコピーして `config.py` にリネームし、必要なら値を変更します：
```python
SERVICE_ACCOUNT_FILE = 'service_account.json'  # 秘密鍵JSONのファイル名
SHEET_NAME = 'AmazonProducts'                  # スプレッドシート名
WORKSHEET_NAME = 'Sheet1'                      # タブ名
```

### 5. 必要ライブラリを入れる（1分）
```
pip install -r requirements.txt
```

### 6. 実行してみる（商品データ→シート）
```
python sync_to_sheets.py
```
- デフォルトでは「ノートパソコン」を最大10件取得してシートに書き込みます
- キーワードや件数を変えたい場合は `sync_to_sheets.py` 内の次の行を編集：
```python
keyword = "ノートパソコン"
max_results = 10
```

### 7. 書き込み結果のイメージ
- 1行目にヘッダー（title, price, rating, review_count, availability, image_url, url, description など）
- 2行目以降に商品データが入ります
- 再実行すると既存の内容をクリアしてから書き込みます（`sync_products(clear_existing=True)` がデフォルト）

### 8. つまずきやすいポイントと対処
- **「権限がありません」と出る**：スプレッドシートの共有設定にサービスアカウントのメールを「編集者」で追加したか確認
- **JSONファイルが見つからない**：`SERVICE_ACCOUNT_FILE` のパスとファイル名を確認
- **403や認証エラーになる**：Google Sheets API を「有効」にしたか、別プロジェクトの鍵を使っていないか確認
- **書き込み順を変えたい/列を増やしたい**：`google_sheets_client.py` の `preferred` リストを編集

これで、取得した商品データをスプレッドシートに定期的に反映できます！

