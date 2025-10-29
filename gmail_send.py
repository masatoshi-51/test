#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gmail API を使用してメールを送信するスクリプト（OAuth2, ユーザー認可）

前提:
- Google Cloud Console で「OAuthクライアントID（デスクトップ）」を作成し、credentials.json を配置
- Gmail API を有効化
- 初回実行時にブラウザで認可し token.json を生成（以後再利用）

使い方（例）:
  python gmail_send.py --to "t.o.u.s08411@ezweb.ne.jp" --subject "テスト" --body "本文です"

引数を省略した場合のデフォルト:
- 宛先: t.o.u.s08411@ezweb.ne.jp（ご指定のアドレス）
- 件名: テスト送信
- 本文: これはGmail APIからのテスト送信です。
"""

import os
import argparse
import base64
from email.mime.text import MIMEText
from typing import List, Optional

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


# 必要最小限のスコープ（送信）
SCOPES: List[str] = [
    "https://www.googleapis.com/auth/gmail.send",
]


def _resolve_credentials_file(preferred_path: str) -> str:
    """指定パスが無ければ、よくある候補名から探索して返す。見つからなければ空文字。"""
    candidates = []
    if preferred_path:
        candidates.append(preferred_path)
    candidates.extend([
        "credentials.json",
        "credentialsaaaaaa.json",
    ])

    script_dir = os.path.dirname(os.path.abspath(__file__))
    for name in list(candidates):
        if not os.path.isabs(name):
            candidates.append(os.path.join(script_dir, name))

    for p in candidates:
        if p and os.path.exists(p):
            return p
    return ""


def load_oauth_credentials(credentials_file: str, token_file: str, scopes: List[str]) -> Credentials:
    """token.json を再利用し、無ければブラウザ認可して保存して返す。"""
    creds: Optional[Credentials] = None

    if os.path.exists(token_file):
        try:
            creds = Credentials.from_authorized_user_file(token_file, scopes)
        except Exception:
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            resolved = _resolve_credentials_file(credentials_file)
            if not resolved:
                raise FileNotFoundError(
                    "OAuthクライアントのcredentials.jsonが見つかりません。--credentials でパスを指定するか、\n"
                    "例: credentials.json または credentialsaaaaaa.json を配置してください。"
                )
            flow = InstalledAppFlow.from_client_secrets_file(resolved, scopes)
            creds = flow.run_local_server(port=0)
        with open(token_file, "w", encoding="utf-8") as f:
            f.write(creds.to_json())
    return creds


def build_gmail_service(creds: Credentials):
    return build("gmail", "v1", credentials=creds)


def create_message(to_addr: str, subject: str, body: str, charset: str = "utf-8") -> dict:
    """MIME メッセージを作成し、Gmail API 送信用の辞書を返す。"""
    msg = MIMEText(body, _charset=charset)
    msg["to"] = to_addr
    msg["subject"] = subject
    # From は省略可能（認可ユーザーのアカウントで送信される）

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")
    return {"raw": raw}


def send_message(service, user_id: str, message: dict) -> dict:
    """メッセージ送信を実行し、APIレスポンスを返す。"""
    return service.users().messages().send(userId=user_id, body=message).execute()


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Gmail 送信（OAuth）")
    p.add_argument("--credentials", default="credentials.json", help="OAuthクライアントのJSONファイル")
    p.add_argument("--token", default="token.json", help="再利用するトークンファイル")
    p.add_argument("--to", default="t.o.u.s08411@ezweb.ne.jp", help="宛先メールアドレス")
    p.add_argument("--subject", default="テスト送信", help="メール件名")
    p.add_argument("--body", default="これはGmail APIからのテスト送信です。", help="メール本文")
    return p.parse_args()


def main():
    args = parse_args()

    creds = load_oauth_credentials(args.credentials, args.token, SCOPES)
    service = build_gmail_service(creds)

    message = create_message(
        to_addr=args.to,
        subject=args.subject,
        body=args.body,
    )

    sent = send_message(service, user_id="me", message=message)
    print("✅ 送信しました")
    print(f"  宛先: {args.to}")
    print(f"  件名: {args.subject}")
    print(f"  メッセージID: {sent.get('id')}")


if __name__ == "__main__":
    main()


