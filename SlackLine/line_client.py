#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LINE Messaging API を使用してメッセージを送信するモジュール
"""

import os
from typing import Optional
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError


def get_line_token() -> str:
    """
    LINE Channel Access Token を取得する。
    優先順位: 環境変数 LINE_CHANNEL_ACCESS_TOKEN > config.py の LINE_CHANNEL_ACCESS_TOKEN
    """
    # 環境変数から取得を試みる
    token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
    if token:
        return token
    
    # config.py から取得を試みる
    try:
        import config
        token = getattr(config, "LINE_CHANNEL_ACCESS_TOKEN", None)
        if token:
            return token
    except ImportError:
        pass
    
    raise RuntimeError(
        "LINE_CHANNEL_ACCESS_TOKEN が設定されていません。\n"
        "環境変数 LINE_CHANNEL_ACCESS_TOKEN を設定するか、\n"
        "config.py に LINE_CHANNEL_ACCESS_TOKEN を設定してください。"
    )


def get_line_user_id() -> str:
    """
    LINE User ID を取得する。
    優先順位: 環境変数 LINE_USER_ID > config.py の LINE_USER_ID
    """
    # 環境変数から取得を試みる
    user_id = os.getenv("LINE_USER_ID")
    if user_id:
        return user_id
    
    # config.py から取得を試みる
    try:
        import config
        user_id = getattr(config, "LINE_USER_ID", None)
        if user_id:
            return user_id
    except ImportError:
        pass
    
    raise RuntimeError(
        "LINE_USER_ID が設定されていません。\n"
        "環境変数 LINE_USER_ID を設定するか、\n"
        "config.py に LINE_USER_ID を設定してください。"
    )


def send_line_message(
    message: str,
    channel_access_token: Optional[str] = None,
    user_id: Optional[str] = None
) -> bool:
    """
    LINE にメッセージを送信する。

    Args:
        message: 送信するメッセージ内容
        channel_access_token: Channel Access Token（未指定の場合は自動取得）
        user_id: 送信先のUser ID（未指定の場合は自動取得）

    Returns:
        送信成功時は True

    Raises:
        LineBotApiError: API呼び出しに失敗した場合
        RuntimeError: Token や User ID が設定されていない場合
    """
    if channel_access_token is None:
        channel_access_token = get_line_token()
    
    if user_id is None:
        user_id = get_line_user_id()
    
    try:
        line_bot_api = LineBotApi(channel_access_token)
        text_message = TextSendMessage(text=message)
        line_bot_api.push_message(user_id, text_message)
        return True
    except LineBotApiError as e:
        error_msg = f"LINE API エラー: {e.status_code} - {e.error.message}"
        if e.status_code == 401:
            error_msg += "\nChannel Access Token が無効です。トークンを確認してください。"
        elif e.status_code == 400:
            error_msg += "\nリクエストが無効です。User ID を確認してください。"
        raise RuntimeError(error_msg) from e


def send_long_message(
    message: str,
    max_length: int = 2000,
    channel_access_token: Optional[str] = None,
    user_id: Optional[str] = None
) -> bool:
    """
    LINE に長いメッセージを送信する（2000文字を超える場合は分割して送信）。

    Args:
        message: 送信するメッセージ内容
        max_length: 1メッセージあたりの最大文字数（デフォルト: 2000）
        channel_access_token: Channel Access Token（未指定の場合は自動取得）
        user_id: 送信先のUser ID（未指定の場合は自動取得）

    Returns:
        送信成功時は True
    """
    if len(message) <= max_length:
        return send_line_message(message, channel_access_token, user_id)
    
    # メッセージを分割
    parts = []
    current_part = ""
    
    for line in message.split("\n"):
        if len(current_part) + len(line) + 1 > max_length:
            if current_part:
                parts.append(current_part)
            current_part = line
        else:
            if current_part:
                current_part += "\n" + line
            else:
                current_part = line
    
    if current_part:
        parts.append(current_part)
    
    # 各部分を送信
    for i, part in enumerate(parts, 1):
        if len(parts) > 1:
            header = f"【{i}/{len(parts)}】\n"
            part = header + part
        send_line_message(part, channel_access_token, user_id)
    
    return True

