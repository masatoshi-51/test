import os
import base64
import json
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import requests


ZOOM_TOKEN_URL = "https://zoom.us/oauth/token"
ZOOM_API_BASE = "https://api.zoom.us/v2"

# 認証情報（テスト用）
ZOOM_ACCOUNT_ID = "KaSDyUKEQKqKioAnmecguQ"
ZOOM_CLIENT_ID = "rnJTvICzQ8CWAkuKLYzNlg"
ZOOM_CLIENT_SECRET = "4TONBjewnSZ1MK5BBph6nS4G1tZJHc6M"


def get_access_token() -> str:
    """Server-to-Server OAuth でアクセストークンを取得する。"""
    print("認証情報を確認中...")
    print(f"Account ID: {ZOOM_ACCOUNT_ID}")
    print(f"Client ID: {ZOOM_CLIENT_ID}")
    print(f"Client Secret: {ZOOM_CLIENT_SECRET[:10]}...")  # 最初の10文字のみ表示
    
    auth_bytes = f"{ZOOM_CLIENT_ID}:{ZOOM_CLIENT_SECRET}".encode("utf-8")
    basic_token = base64.b64encode(auth_bytes).decode("utf-8")
    
    print(f"Basic Token: {basic_token[:20]}...")  # 最初の20文字のみ表示

    headers = {
        "Authorization": f"Basic {basic_token}",
    }
    params = {
        "grant_type": "account_credentials",
        "account_id": ZOOM_ACCOUNT_ID,
    }

    print("Zoom APIにリクエスト送信中...")
    print(f"URL: {ZOOM_TOKEN_URL}")
    print(f"Params: {params}")
    
    resp = requests.post(ZOOM_TOKEN_URL, headers=headers, params=params, timeout=30)
    
    print(f"レスポンス ステータス: {resp.status_code}")
    print(f"レスポンス 内容: {resp.text}")
    
    if resp.status_code != 200:
        raise RuntimeError(f"トークン取得に失敗しました: {resp.status_code} {resp.text}")

    data = resp.json()
    access_token = data.get("access_token")
    if not access_token:
        raise RuntimeError("レスポンスに access_token が含まれていません")
    
    print("アクセストークンの取得に成功しました！")
    return access_token


def create_meeting(
    *,
    topic: str,
    start_time: Optional[datetime] = None,
    duration_min: int = 60,
    timezone_str: Optional[str] = None,
    password: Optional[str] = None,
) -> Dict[str, Any]:
    """Zoom 会議を作成し、レスポンスを返す。"""
    token = get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    if start_time is None:
        start_dt = datetime.now(timezone.utc) + timedelta(minutes=5)
    else:
        start_dt = start_time if start_time.tzinfo else start_time.replace(tzinfo=timezone.utc)

    start_time_str = start_dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    payload: Dict[str, Any] = {
        "topic": topic,
        "type": 2,  # Scheduled meeting
        "start_time": start_time_str,
        "duration": duration_min,
    }

    if timezone_str:
        payload["timezone"] = timezone_str
    if password:
        payload["password"] = password

    payload["settings"] = {
        "host_video": False,
        "participant_video": False,
        "waiting_room": False,
        "join_before_host": True,
        "mute_upon_entry": True,
        "approval_type": 2,  # No registration required
    }

    url = f"{ZOOM_API_BASE}/users/me/meetings"

    resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
    
    print(f"会議作成レスポンス ステータス: {resp.status_code}")
    print(f"会議作成レスポンス 内容: {resp.text}")
    
    if resp.status_code not in (200, 201):
        error_msg = f"会議作成に失敗しました: {resp.status_code} {resp.text}"
        
        # スコープエラーの場合の詳細説明
        if "4711" in resp.text and "scopes" in resp.text:
            error_msg += "\n\n【解決方法】\n"
            error_msg += "1. Zoom Marketplace でアプリの Scopes タブを開く\n"
            error_msg += "2. 以下のスコープを有効にする:\n"
            error_msg += "   - meeting:write:meeting\n"
            error_msg += "   - meeting:write:meeting:admin\n"
            error_msg += "3. Save をクリック\n"
            error_msg += "4. Activation タブでアプリを再アクティベート\n"
        
        raise RuntimeError(error_msg)

    return resp.json()


def print_meeting_summary(meeting: Dict[str, Any]) -> None:
    meeting_id = meeting.get("id")
    password = meeting.get("password")
    join_url = meeting.get("join_url")
    start_url = meeting.get("start_url")

    print("=== Zoom 会議が作成されました ===")
    print(f"Meeting ID: {meeting_id}")
    print(f"Password  : {password}")
    print(f"Join URL  : {join_url}")
    print(f"Start URL : {start_url}")


if __name__ == "__main__":
    try:
        print("Zoom 会議を作成中...")
        meeting = create_meeting(
            topic="テスト会議",
            duration_min=30,
        )
        print_meeting_summary(meeting)
    except Exception as e:
        print(f"エラーが発生しました: {e}")
