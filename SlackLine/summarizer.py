#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
メッセージを要約するモジュール
"""

from typing import List, Dict


def summarize_messages(messages: List[Dict], max_length: int = 1000) -> str:
    """
    メッセージリストを要約する。

    Args:
        messages: メッセージのリスト
        max_length: 要約の最大文字数（デフォルト: 1000）

    Returns:
        要約された文字列
    """
    if not messages:
        return "メッセージがありません。"
    
    from datetime import datetime
    
    total_messages = len(messages)
    users = set()
    
    # ユーザー数をカウント
    for msg in messages:
        users.add(msg['user'])
    
    # 要約ヘッダー
    summary_lines = [f"📬 Slackメッセージ要約\n"]
    summary_lines.append("=" * 40)
    summary_lines.append(f"📊 総メッセージ数: {total_messages}件")
    summary_lines.append(f"👥 参加者数: {len(users)}名")
    
    # 時間範囲を表示
    if messages:
        first_time = datetime.fromtimestamp(messages[-1]["timestamp"])
        last_time = datetime.fromtimestamp(messages[0]["timestamp"])
        summary_lines.append(f"⏰ 期間: {first_time.strftime('%m/%d %H:%M')} ～ {last_time.strftime('%m/%d %H:%M')}")
    
    summary_lines.append("=" * 40)
    summary_lines.append("")
    
    # メッセージが少ない場合（5件以下）
    if total_messages <= 5:
        summary_lines.append("【メッセージ内容】")
        for msg in messages:
            dt = datetime.fromtimestamp(msg["timestamp"])
            time_str = dt.strftime("%m/%d %H:%M")
            text = msg['text'].replace('\n', ' ').strip()
            # 長いメッセージは切り詰め
            if len(text) > 150:
                text = text[:150] + "..."
            summary_lines.append(f"• [{time_str}] {msg['user']}: {text}")
    
    # メッセージが多い場合（6件以上）
    else:
        summary_lines.append("【最新のメッセージ（最初の3件）】")
        for msg in messages[:3]:
            dt = datetime.fromtimestamp(msg["timestamp"])
            time_str = dt.strftime("%m/%d %H:%M")
            text = msg['text'].replace('\n', ' ').strip()
            if len(text) > 120:
                text = text[:120] + "..."
            summary_lines.append(f"• [{time_str}] {msg['user']}: {text}")
        
        summary_lines.append("")
        summary_lines.append(f"... 他 {total_messages - 6}件のメッセージ ...")
        summary_lines.append("")
        
        summary_lines.append("【最新のメッセージ（最後の3件）】")
        for msg in messages[-3:]:
            dt = datetime.fromtimestamp(msg["timestamp"])
            time_str = dt.strftime("%m/%d %H:%M")
            text = msg['text'].replace('\n', ' ').strip()
            if len(text) > 120:
                text = text[:120] + "..."
            summary_lines.append(f"• [{time_str}] {msg['user']}: {text}")
    
    summary = "\n".join(summary_lines)
    
    # 最大文字数を超える場合は切り詰め
    if len(summary) > max_length:
        summary = summary[:max_length] + "\n\n...（要約が長すぎるため一部を省略）"
    
    return summary


def create_simple_summary(messages: List[Dict]) -> str:
    """
    シンプルな要約を作成する（要約機能を使わない場合）。

    Args:
        messages: メッセージのリスト

    Returns:
        フォーマットされた文字列
    """
    if not messages:
        return "メッセージがありません。"
    
    from datetime import datetime
    
    summary_lines = [f"📬 Slackメッセージ通知 ({len(messages)}件)\n"]
    summary_lines.append("=" * 30 + "\n")
    
    for msg in messages:
        dt = datetime.fromtimestamp(msg["timestamp"])
        time_str = dt.strftime("%m/%d %H:%M")
        text = msg['text'][:200] + ("..." if len(msg['text']) > 200 else "")
        summary_lines.append(f"[{time_str}] {msg['user']}\n{text}\n")
    
    return "\n".join(summary_lines)

