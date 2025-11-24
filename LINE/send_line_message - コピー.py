"""
LINE Messaging API を使って、テキストメッセージを1通送るだけのシンプルなサンプル。
使い方は README.md を参照してください。
"""

from linebot import LineBotApi
from linebot.models import TextSendMessage

# TODO: 自分のチャネルアクセストークンを貼り付ける
CHANNEL_ACCESS_TOKEN = ""

# TODO: 送りたい相手（自分）のユーザーIDを貼り付ける
USER_ID = ""


def send_message() -> None:
    """LINE にテキストメッセージを送ります。"""
    if "YOUR_CHANNEL_ACCESS_TOKEN" in CHANNEL_ACCESS_TOKEN:
        raise ValueError("CHANNEL_ACCESS_TOKEN を正しく設定してください。")
    if "TARGET_USER_ID" in USER_ID:
        raise ValueError("USER_ID を正しく設定してください。")

    line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
    message = TextSendMessage(text="こんにちは！PythonからLINEを送ってみたよ。")
    line_bot_api.push_message(USER_ID, message)
    print("メッセージを送信しました。LINEを確認してください。")


if __name__ == "__main__":
    send_message()

