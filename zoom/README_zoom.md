## Zoom 会議作成スクリプトの使い方

このフォルダには、ZoomのServer-to-Server OAuthを用いて会議を作成するスクリプト `zoom_create_meeting.py` が入っています。作成後に Meeting ID、パスワード、参加リンクを出力します。

### 1. 前提: Zoom 側設定
- Zoom Marketplace で「Server-to-Server OAuth」アプリを作成
- App Credentials の `Account ID`、`Client ID`、`Client Secret` を取得
- App で必要なスコープに最低限 `meeting:write:admin` を含める

### 2. 環境変数を設定
以下をOSの環境変数、または `.env` に設定してください。

```
ZOOM_ACCOUNT_ID=xxxx
ZOOM_CLIENT_ID=xxxx
ZOOM_CLIENT_SECRET=xxxx
# 任意: 対象ユーザーを固定したい場合（メールアドレス or "me"）
ZOOM_USER_ID=me
```

`.env` を使う場合は、このフォルダと同じ場所に `.env` を置きます。

### 3. 依存関係のインストール

```
pip install -r requirements_zoom.txt
```

### 4. 実行例

```
python zoom_create_meeting.py --topic "打合せ" --start_time 2025-10-13T09:00 --duration 45
```

タイムゾーンを指定する例:

```
python zoom_create_meeting.py --topic "打合せ" --start_time 2025-10-13T18:00 --timezone Asia/Tokyo
```

出力例:

```
=== Zoom 会議が作成されました ===
Meeting ID: 123456789
Password  : 1AbCd2
Join URL  : https://zoom.us/j/123456789?pwd=...
```

### 備考
- `--start_time` を省略すると現在時刻の5分後開始で作成します（UTC基準）
- エラーが出た場合は、スコープ、資格情報の有効性、組織のポリシー制限をご確認ください

