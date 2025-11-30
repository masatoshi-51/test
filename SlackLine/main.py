#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Slackチャンネルからメッセージを取得し、LINEに送信するメインプログラム
"""

import argparse
import sys
from slack_client import get_channel_messages, format_messages_for_display
from line_client import send_long_message
from summarizer import summarize_messages, create_simple_summary


def parse_args() -> argparse.Namespace:
    """コマンドライン引数を解析する"""
    parser = argparse.ArgumentParser(
        description="Slackチャンネルからメッセージを取得し、LINEに送信する",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # デフォルト設定で実行（過去24時間のメッセージを取得してLINEに送信）
  python main.py --channel "#general"
  
  # 過去12時間のメッセージを取得
  python main.py --channel "#general" --hours 12
  
  # 要約機能を使わずに全てのメッセージを送信
  python main.py --channel "#general" --no-summary
  
  # 最大50件のメッセージを取得
  python main.py --channel "#general" --limit 50
        """
    )
    parser.add_argument(
        "--channel", "-c",
        required=True,
        help="Slackチャンネル名（#general）またはチャンネルID（C1234567890）"
    )
    parser.add_argument(
        "--hours", "-H",
        type=int,
        default=24,
        help="何時間前までのメッセージを取得するか（デフォルト: 24）"
    )
    parser.add_argument(
        "--limit", "-l",
        type=int,
        default=100,
        help="取得するメッセージの最大数（デフォルト: 100）"
    )
    parser.add_argument(
        "--no-summary",
        action="store_true",
        help="要約機能を使わずに全てのメッセージを送信する"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="実際にLINEに送信せず、内容を表示するだけ"
    )
    return parser.parse_args()


def main():
    """メイン処理"""
    args = parse_args()
    
    try:
        print(f"📥 Slackチャンネル '{args.channel}' からメッセージを取得中...")
        
        # Slackからメッセージを取得
        messages = get_channel_messages(
            channel=args.channel,
            hours=args.hours,
            limit=args.limit
        )
        
        if not messages:
            print("ℹ️  メッセージが見つかりませんでした。")
            return
        
        print(f"✅ {len(messages)}件のメッセージを取得しました")
        
        # メッセージをフォーマット
        if args.no_summary:
            # 要約なしで全て送信
            formatted_message = create_simple_summary(messages)
        else:
            # 要約して送信
            formatted_message = summarize_messages(messages)
        
        # ドライラン（テスト実行）の場合は表示のみ
        if args.dry_run:
            print("\n" + "=" * 50)
            print("【送信予定のメッセージ】")
            print("=" * 50)
            print(formatted_message)
            print("=" * 50)
            print("\n✅ ドライラン完了（実際には送信されませんでした）")
            return
        
        # LINEに送信
        print("📤 LINEにメッセージを送信中...")
        send_long_message(formatted_message)
        print("✅ LINEへの送信が完了しました！")
        
    except RuntimeError as e:
        print(f"❌ エラー: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️  処理が中断されました。")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 予期しないエラーが発生しました: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

