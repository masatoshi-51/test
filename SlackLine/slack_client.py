#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Slack API を使用してチャンネルからメッセージを取得するモジュール
"""

import os
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


def get_slack_token() -> str:
    """
    Slack Bot Token を取得する。
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


def get_channel_messages(
    channel: str,
    hours: int = 24,
    limit: int = 100,
    bot_token: Optional[str] = None
) -> List[Dict]:
    """
    Slackチャンネルからメッセージを取得する。

    Args:
        channel: チャンネル名（#general）またはチャンネルID（C1234567890）
        hours: 何時間前までのメッセージを取得するか（デフォルト: 24時間）
        limit: 取得するメッセージの最大数（デフォルト: 100）
        bot_token: Bot Token（未指定の場合は自動取得）

    Returns:
        メッセージのリスト。各メッセージは辞書形式で以下のキーを持つ:
        - text: メッセージ本文
        - user: ユーザー名
        - timestamp: タイムスタンプ
        - channel: チャンネル名

    Raises:
        SlackApiError: API呼び出しに失敗した場合
        RuntimeError: Bot Token が設定されていない場合
    """
    if bot_token is None:
        bot_token = get_slack_token()
    
    client = WebClient(token=bot_token)
    
    try:
        # チャンネル名が # で始まる場合は、# を削除
        channel_name = channel[1:] if channel.startswith("#") else channel
        
        # チャンネルIDを取得
        channel_id = None
        if not channel_name.startswith("C"):
            # チャンネル名からIDを取得
            try:
                result = client.conversations_list(types="public_channel,private_channel")
                for ch in result["channels"]:
                    if ch["name"] == channel_name:
                        channel_id = ch["id"]
                        break
                if not channel_id:
                    raise RuntimeError(f"チャンネル '{channel}' が見つかりません。")
            except SlackApiError as e:
                error_code = e.response.get("error", "unknown_error")
                if error_code == "missing_scope":
                    raise RuntimeError(
                        f"必要な権限（スコープ）が不足しています。\n"
                        f"Slack Appの設定で以下のスコープを追加してください：\n"
                        f"  - channels:read（公開チャンネルの情報を読み取る）\n"
                        f"  - groups:read（プライベートチャンネルの情報を読み取る）\n\n"
                        f"または、チャンネルIDを直接指定してください。\n"
                        f"例: python main.py --channel \"C1234567890\""
                    ) from e
                else:
                    raise RuntimeError(f"チャンネル情報の取得に失敗しました: {error_code}") from e
        else:
            channel_id = channel_name
        
        # 指定時間前のタイムスタンプを計算
        oldest_timestamp = (datetime.now() - timedelta(hours=hours)).timestamp()
        
        # メッセージを取得
        response = client.conversations_history(
            channel=channel_id,
            oldest=str(oldest_timestamp),
            limit=limit
        )
        
        messages = []
        for msg in response["messages"]:
            # ボットメッセージや削除されたメッセージは除外
            if msg.get("subtype") in ["bot_message", "message_deleted"]:
                continue
            
            # ユーザー情報を取得
            user_name = "不明"
            if "user" in msg:
                try:
                    user_info = client.users_info(user=msg["user"])
                    user_name = user_info["user"]["real_name"] or user_info["user"]["name"]
                except SlackApiError:
                    user_name = msg["user"]
            
            messages.append({
                "text": msg.get("text", ""),
                "user": user_name,
                "timestamp": float(msg.get("ts", 0)),
                "channel": channel
            })
        
        return messages
        
    except SlackApiError as e:
        error_msg = f"Slack API エラー: {e.response['error']}"
        if e.response.get("error") == "channel_not_found":
            error_msg += f"\nチャンネル '{channel}' が見つかりません。チャンネルIDを確認するか、ボットをチャンネルに追加してください。"
        elif e.response.get("error") == "not_in_channel":
            error_msg += f"\nボットがチャンネル '{channel}' に参加していません。チャンネルにボットを追加してください。"
        elif e.response.get("error") == "invalid_auth":
            error_msg += "\nBot Token が無効です。トークンを確認してください。"
        raise RuntimeError(error_msg) from e


def format_messages_for_display(messages: List[Dict]) -> str:
    """
    メッセージリストを表示用の文字列にフォーマットする。

    Args:
        messages: get_channel_messages() で取得したメッセージリスト

    Returns:
        フォーマットされた文字列
    """
    if not messages:
        return "メッセージが見つかりませんでした。"
    
    formatted_lines = []
    for msg in messages:
        dt = datetime.fromtimestamp(msg["timestamp"])
        time_str = dt.strftime("%Y-%m-%d %H:%M")
        formatted_lines.append(f"[{time_str}] {msg['user']}: {msg['text']}")
    
    return "\n".join(formatted_lines)

