#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Slack API を使用して指定のチャンネルにメッセージを投稿するスクリプト

前提:
- Slack App を作成し、Bot Token を取得
- Bot Token を config.py または環境変数 SLACK_BOT_TOKEN に設定
- ボットを対象チャンネルに追加

使い方（例）:
  python slack_send_message.py --channel "#general" --message "テストメッセージ"
  python slack_send_message.py --channel "C1234567890" --message "チャンネルIDで指定"
"""

import os
import argparse
from typing import Optional

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def get_bot_token() -> str:
    """
    Bot Token を取得する。
    優先順位: 環境変数 SLACK_BOT_TOKEN > config.py の SLACK_BOT_TOKEN
    """
    # 環境変数から取得を試みる
    token = os.getenv("SLACK_BOT_TOKEN")
    if token:
        return token
    
    # config.py から取得を試みる
    try:
        import config
        token = getattr(config, "SLACK_BOT_TOKEN", None)
        if token:
            return token
    except ImportError:
        pass
    
    raise RuntimeError(
        "SLACK_BOT_TOKEN が設定されていません。\n"
        "環境変数 SLACK_BOT_TOKEN を設定するか、\n"
        "config.py に SLACK_BOT_TOKEN を設定してください。"
    )


def send_message(
    channel: str,
    message: str,
    thread_ts: Optional[str] = None,
    bot_token: Optional[str] = None,
) -> dict:
    """
    Slack チャンネルにメッセージを投稿する。

    Args:
        channel: チャンネル名（#general）またはチャンネルID（C1234567890）
        message: 投稿するメッセージ内容
        thread_ts: スレッドのタイムスタンプ（スレッド返信の場合）
        bot_token: Bot Token（未指定の場合は自動取得）

    Returns:
        APIレスポンス（成功時）

    Raises:
        SlackApiError: API呼び出しに失敗した場合
        RuntimeError: Bot Token が設定されていない場合
    """
    if bot_token is None:
        bot_token = get_bot_token()
    
    client = WebClient(token=bot_token)
    
    try:
        # チャンネル名が # で始まる場合は、# を削除
        if channel.startswith("#"):
            channel = channel[1:]
        
        payload = {
            "channel": channel,
            "text": message,
        }
        
        if thread_ts:
            payload["thread_ts"] = thread_ts
        
        response = client.chat_postMessage(**payload)
        return response.data
        
    except SlackApiError as e:
        error_msg = f"Slack API エラー: {e.response['error']}"
        if e.response.get("error") == "channel_not_found":
            error_msg += f"\nチャンネル '{channel}' が見つかりません。チャンネルIDを確認するか、ボットをチャンネルに追加してください。"
        elif e.response.get("error") == "not_in_channel":
            error_msg += f"\nボットがチャンネル '{channel}' に参加していません。チャンネルにボットを追加してください。"
        elif e.response.get("error") == "invalid_auth":
            error_msg += "\nBot Token が無効です。トークンを確認してください。"
        raise RuntimeError(error_msg) from e


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Slack チャンネルにメッセージを投稿する",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # チャンネル名で指定
  python slack_send_message.py --channel "#general" --message "こんにちは"
  
  # チャンネルIDで指定
  python slack_send_message.py --channel "C1234567890" --message "テスト"
  
  # スレッドに返信
  python slack_send_message.py --channel "#general" --message "返信" --thread "1234567890.123456"
        """
    )
    parser.add_argument(
        "--channel", "-c",
        required=True,
        help="チャンネル名（#general）またはチャンネルID（C1234567890）"
    )
    parser.add_argument(
        "--message", "-m",
        required=True,
        help="投稿するメッセージ内容"
    )
    parser.add_argument(
        "--thread", "-t",
        help="スレッドのタイムスタンプ（スレッド返信の場合）"
    )
    parser.add_argument(
        "--token",
        help="Bot Token（未指定の場合は環境変数またはconfig.pyから取得）"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="出力を最小限にする（エラー時のみ表示）"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    
    try:
        bot_token = args.token or get_bot_token()
        response = send_message(
            channel=args.channel,
            message=args.message,
            thread_ts=args.thread,
            bot_token=bot_token,
        )
        
        if not args.quiet:
            print("✅ メッセージを投稿しました")
            print(f"  チャンネル: {args.channel}")
            print(f"  メッセージ: {args.message}")
            if "ts" in response:
                print(f"  タイムスタンプ: {response['ts']}")
            if "channel" in response:
                print(f"  チャンネルID: {response['channel']}")
        else:
            print("✅ 投稿完了")
            
    except (RuntimeError, SlackApiError) as e:
        print(f"❌ エラー: {e}")
        exit(1)


if __name__ == "__main__":
    main()

