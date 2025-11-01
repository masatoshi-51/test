# YouTube Data API 動画検索スクリプト

このプロジェクトは、YouTube Data APIを使用して動画を検索し、タイトルとURLを表示するPythonスクリプトです。

## 📋 目次

1. [前提条件](#前提条件)
2. [セットアップ手順](#セットアップ手順)
3. [使用方法](#使用方法)
4. [トラブルシューティング](#トラブルシューティング)

## 前提条件

- Python 3.6以上がインストールされていること
- Googleアカウントを持っていること
- インターネット接続があること

## セットアップ手順

### ステップ1: YouTube Data APIキーの取得

1. **Google Cloud Consoleにアクセス**
   - ブラウザで [Google Cloud Console](https://console.cloud.google.com/) にアクセス
   - Googleアカウントでログインします

2. **プロジェクトの作成**
   - 画面右上のプロジェクト選択メニューをクリック
   - 「新しいプロジェクト」を選択
   - プロジェクト名を入力（例: "YouTube Search Project"）
   - 「作成」をクリック
   - 作成したプロジェクトを選択

3. **YouTube Data API v3を有効化**
   - 左側のメニューから「APIとサービス」>「ライブラリ」を選択
   - 検索バーで「YouTube Data API v3」を検索
   - 「YouTube Data API v3」をクリック
   - 「有効にする」ボタンをクリック

4. **APIキーの作成**
   - 左側のメニューから「APIとサービス」>「認証情報」を選択
   - 画面上部の「認証情報を作成」をクリック
   - 「APIキー」を選択
   - 作成されたAPIキーが表示されます（コピーしておく）
   - **重要**: APIキーの制限を設定することをお勧めします
     - 「APIキーを制限」をクリック
     - 「APIの制限」タブで「キーを制限」を選択
     - 「YouTube Data API v3」のみにチェックを入れ、「保存」をクリック

### ステップ2: 依存パッケージのインストール

ターミナルまたはコマンドプロンプトを開き、このディレクトリに移動して以下を実行：

```bash
pip install -r requirements.txt
```

または、個別にインストールする場合：

```bash
pip install google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2
```

### ステップ3: APIキーの設定

1. `config.py` ファイルを開く
2. `YOUR_API_KEY_HERE` を、ステップ1で取得したAPIキーに置き換える

```python
YOUTUBE_API_KEY = "あなたのAPIキーをここに貼り付け"
```

**注意**: 
- APIキーは機密情報です。GitHubなどの公開リポジトリにコミットしないでください
- `config.py` を `.gitignore` に追加することをお勧めします

## 使用方法

1. ターミナルまたはコマンドプロンプトで、このディレクトリに移動

2. スクリプトを実行：

```bash
python youtube_search.py
```

3. 検索キーワードを入力（例: "Python チュートリアル"）

4. 取得する結果数を入力（何も入力せずEnterを押すと、デフォルトの10件が取得されます）

5. 検索結果が表示されます

### 実行例

```
検索キーワードを入力してください: Python チュートリアル
取得する結果数（デフォルト: 10）: 5

「Python チュートリアル」を検索中...

=== 検索結果 (5件) ===

1. 【Python超入門コース】初心者向けに基本から実践まで解説
   URL: https://www.youtube.com/watch?v=xxxxx

2. Python入門 - 初心者向け完全ガイド
   URL: https://www.youtube.com/watch?v=xxxxx

...
```

## トラブルシューティング

### エラー: `APIリクエストでエラーが発生しました`

- APIキーが正しく設定されているか確認してください
- YouTube Data API v3が有効になっているか確認してください
- APIキーの使用制限に達していないか確認してください（無料枠は1日10,000ユニット）

### エラー: `ModuleNotFoundError: No module named 'googleapiclient'`

依存パッケージがインストールされていません。以下を実行してください：

```bash
pip install -r requirements.txt
```

### 検索結果が表示されない

- インターネット接続を確認してください
- APIキーにAPIの制限が正しく設定されているか確認してください
- キーワードを変更して再度試してみてください

### APIクォータ制限について

YouTube Data API v3の無料枠は、1日あたり10,000ユニット（クォータ単位）です。
- 1回の検索リクエスト = 100ユニット
- つまり、1日あたり約100回の検索が可能です

## カスタマイズ

### 検索結果の並び順を変更

`youtube_search.py` の `order` パラメータを変更することで、並び順を変更できます：

- `'relevance'`: 関連度順（デフォルト）
- `'date'`: アップロード日時順（新しい順）
- `'rating'`: 評価順
- `'viewCount'`: 再生回数順
- `'title'`: タイトル順

### コマンドライン引数からキーワードを受け取る

スクリプトをコマンドライン引数からもキーワードを受け取れるようにカスタマイズすることもできます。

## 参考リンク

- [YouTube Data API v3 ドキュメント](https://developers.google.com/youtube/v3)
- [Google Cloud Console](https://console.cloud.google.com/)
- [APIクォータの詳細](https://developers.google.com/youtube/v3/getting-started#quota)

