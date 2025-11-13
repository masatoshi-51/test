#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Slack 接続テストスクリプト

このスクリプトは、設定が正しいかどうかを確認するための簡単なテストです。
実際にメッセージを送信せずに、接続だけを確認します。
"""

import sys
import os

def check_current_directory():
    """現在のディレクトリが正しいか確認"""
    current_dir = os.getcwd()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 現在のディレクトリに必要なファイルがあるか確認
    required_files = ["config.py", "slack_send_message.py", "test_connection.py"]
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("=" * 50)
        print("⚠️  警告: 必要なファイルが見つかりません")
        print("=" * 50)
        print(f"現在のディレクトリ: {current_dir}")
        print(f"スクリプトの場所: {script_dir}")
        print(f"\n見つからないファイル:")
        for file in missing_files:
            print(f"  - {file}")
        print(f"\n💡 解決方法:")
        print(f"   以下のコマンドで slack フォルダに移動してください：")
        print(f'   cd "{script_dir}"')
        print("=" * 50 + "\n")
        return False
    
    return True


def test_config():
    """config.py が正しく設定されているか確認"""
    print("=" * 50)
    print("📋 ステップ1: config.py の確認")
    print("=" * 50)
    
    try:
        import config
        token = getattr(config, "SLACK_BOT_TOKEN", None)
        
        if not token:
            print("❌ SLACK_BOT_TOKEN が設定されていません")
            print("   config.py に Bot Token を設定してください")
            return False
        
        if token == "":
            print("❌ SLACK_BOT_TOKEN が空です")
            print("   config.py に Bot Token を設定してください")
            return False
        
        if not token.startswith("xoxb-"):
            print("⚠️  Bot Token の形式が正しくない可能性があります")
            print(f"   現在のトークン: {token[:10]}...")
            print("   Bot Token は 'xoxb-' で始まる必要があります")
        else:
            print("✅ config.py に Bot Token が設定されています")
            print(f"   トークン: {token[:15]}...")
        
        return True
        
    except ImportError:
        print("❌ config.py が見つかりません")
        return False
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False


def test_environment():
    """環境変数が設定されているか確認"""
    print("\n" + "=" * 50)
    print("📋 ステップ2: 環境変数の確認")
    print("=" * 50)
    
    token = os.getenv("SLACK_BOT_TOKEN")
    if token:
        print("✅ 環境変数 SLACK_BOT_TOKEN が設定されています")
        print(f"   トークン: {token[:15]}...")
        return True
    else:
        print("ℹ️  環境変数 SLACK_BOT_TOKEN は設定されていません（config.py を使用）")
        return False


def test_package():
    """必要なパッケージがインストールされているか確認"""
    print("\n" + "=" * 50)
    print("📋 ステップ3: パッケージの確認")
    print("=" * 50)
    
    try:
        import slack_sdk
        print("✅ slack-sdk がインストールされています")
        print(f"   バージョン: {slack_sdk.__version__}")
        return True
    except ImportError:
        print("❌ slack-sdk がインストールされていません")
        print("   以下のコマンドを実行してください：")
        print("   pip install -r requirements.txt")
        return False


def test_connection():
    """Slack API への接続をテスト"""
    print("\n" + "=" * 50)
    print("📋 ステップ4: Slack API への接続テスト")
    print("=" * 50)
    
    try:
        from slack_sdk import WebClient
        from slack_sdk.errors import SlackApiError
        
        # トークンを取得
        try:
            import config
            token = getattr(config, "SLACK_BOT_TOKEN", None)
        except ImportError:
            token = os.getenv("SLACK_BOT_TOKEN")
        
        if not token:
            print("❌ Bot Token が取得できませんでした")
            return False
        
        # クライアントを作成
        client = WebClient(token=token)
        
        # auth.test を実行して接続を確認
        print("   接続を確認中...")
        response = client.auth_test()
        
        if response["ok"]:
            print("✅ Slack API への接続に成功しました！")
            print(f"   ワークスペース: {response.get('team', 'N/A')}")
            print(f"   ユーザー: {response.get('user', 'N/A')}")
            print(f"   ボットID: {response.get('bot_id', 'N/A')}")
            return True
        else:
            print("❌ 接続に失敗しました")
            return False
            
    except SlackApiError as e:
        error = e.response.get("error", "unknown")
        if error == "invalid_auth":
            print("❌ Bot Token が無効です")
            print("   config.py のトークンが正しいか確認してください")
        else:
            print(f"❌ Slack API エラー: {error}")
        return False
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False


def main():
    """メイン関数"""
    print("\n" + "🔍 Slack 接続テストを開始します" + "\n")
    
    # まず、現在のディレクトリを確認
    if not check_current_directory():
        print("❌ テストを中断しました。上記の指示に従って、slack フォルダに移動してください。")
        return 1
    
    results = []
    
    # 各テストを実行
    results.append(("config.py", test_config()))
    results.append(("環境変数", test_environment()))
    results.append(("パッケージ", test_package()))
    results.append(("接続", test_connection()))
    
    # 結果をまとめる
    print("\n" + "=" * 50)
    print("📊 テスト結果のまとめ")
    print("=" * 50)
    
    all_ok = True
    for name, result in results:
        status = "✅ OK" if result else "❌ NG"
        print(f"   {name}: {status}")
        if not result:
            all_ok = False
    
    print("\n" + "=" * 50)
    if all_ok:
        print("🎉 すべてのテストに合格しました！")
        print("   メッセージを送信する準備ができています。")
        print("\n   試しにメッセージを送信するには：")
        print('   python slack_send_message.py --channel "#チャンネル名" --message "テスト"')
    else:
        print("⚠️  いくつかのテストに失敗しました")
        print("   上記のエラーメッセージを確認して、問題を解決してください。")
        print("\n   詳細は以下を参照してください：")
        print("   - 完全ガイド_初心者向け.md")
        print("   - 状態確認チェックリスト.md")
    print("=" * 50 + "\n")
    
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())

