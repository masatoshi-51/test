import os
import base64
import json
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import requests


ZOOM_TOKEN_URL = "https://zoom.us/oauth/token"
ZOOM_API_BASE = "https://api.zoom.us/v2"


def _get_env(name: str, required: bool = True, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name, default)
    if required and not value:
        raise RuntimeError(f"環境変数 {name} が設定されていません")
    return value


def get_access_token() -> str:
    """Server-to-Server OAuth でアクセストークンを取得する。"""
    account_id = _get_env("ZOOM_ACCOUNT_ID")
    client_id = _get_env("ZOOM_CLIENT_ID")
    client_secret = _get_env("ZOOM_CLIENT_SECRET")

    auth_bytes = f"{client_id}:{client_secret}".encode("utf-8")
    basic_token = base64.b64encode(auth_bytes).decode("utf-8")

    headers = {
        "Authorization": f"Basic {basic_token}",
    }
    params = {
        "grant_type": "account_credentials",
        "account_id": account_id,
    }

    resp = requests.post(ZOOM_TOKEN_URL, headers=headers, params=params, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(f"トークン取得に失敗しました: {resp.status_code} {resp.text}")

    data = resp.json()
    access_token = data.get("access_token")
    if not access_token:
        raise RuntimeError("レスポンスに access_token が含まれていません")
    return access_token


def create_meeting(
    *,
    topic: str,
    start_time: Optional[datetime] = None,
    duration_min: int = 60,
    timezone_str: Optional[str] = None,
    password: Optional[str] = None,
    user_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Zoom 会議を作成し、レスポンスを返す。

    戻り値の主なキー:
      - id: 数値のミーティングID（例: 123456789）
      - password: ミーティングパスワード
      - join_url: 参加用URL
      - start_url: ホスト用開始URL
    """
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
        "type": 2,
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
        "approval_type": 2,
    }

    target_user = user_id or os.getenv("ZOOM_USER_ID") or "me"
    url = f"{ZOOM_API_BASE}/users/{target_user}/meetings"

    resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
    if resp.status_code not in (200, 201):
        raise RuntimeError(f"会議作成に失敗しました: {resp.status_code} {resp.text}")

    return resp.json()


def print_meeting_summary(meeting: Dict[str, Any]) -> None:
    meeting_id = meeting.get("id")
    password = meeting.get("password")
    join_url = meeting.get("join_url")

    print("=== Zoom 会議が作成されました ===")
    print(f"Meeting ID: {meeting_id}")
    print(f"Password  : {password}")
    print(f"Join URL  : {join_url}")


def _parse_iso_datetime(value: str) -> datetime:
    try:
        if len(value) == 16:
            return datetime.strptime(value, "%Y-%m-%dT%H:%M").replace(tzinfo=timezone.utc)
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
    except ValueError as exc:
        raise ValueError("start_time は ISO8601 (例: 2025-10-13T09:00) で指定してください") from exc


if __name__ == "__main__":
    import argparse

    try:
        from dotenv import load_dotenv  # type: ignore
        load_dotenv()
    except Exception:
        pass

    parser = argparse.ArgumentParser(description="Zoom 会議を作成するツール")
    parser.add_argument("--topic", required=True, help="会議タイトル")
    parser.add_argument("--start_time", help="開始日時 (ISO8601, 例: 2025-10-13T09:00)")
    parser.add_argument("--duration", type=int, default=60, help="会議時間(分)")
    parser.add_argument("--timezone", dest="tz", help="タイムゾーン (例: Asia/Tokyo)")
    parser.add_argument("--password", help="会議パスワード (任意)")
    parser.add_argument("--user_id", help="対象ユーザー(メールまたは me)。未指定なら ZOOM_USER_ID か me")

    args = parser.parse_args()

    dt = _parse_iso_datetime(args.start_time) if args.start_time else None
    meeting = create_meeting(
        topic=args.topic,
        start_time=dt,
        duration_min=args.duration,
        timezone_str=args.tz,
        password=args.password,
        user_id=args.user_id,
    )
    print_meeting_summary(meeting)


