"""
ユーザーが送った「◯時に△△する」の内容に合わせてリマインドを返すサンプルボット。
例: 「10時に宿題をやる」「15:30に散歩する」など。
"""

from __future__ import annotations

import os
import re
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, abort, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

JST = timezone(timedelta(hours=9))

# --- 1. LINEの秘密の情報をここで設定 ---
CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "")
CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET", "")

if "YOUR_CHANNEL_ACCESS_TOKEN" in CHANNEL_ACCESS_TOKEN:
    raise ValueError("CHANNEL_ACCESS_TOKEN を reminder_bot.py に設定してください。")
if "YOUR_CHANNEL_SECRET" in CHANNEL_SECRET:
    raise ValueError("CHANNEL_SECRET を reminder_bot.py に設定してください。")

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# --- 2. 予定を覚えておくタイマーを用意 ---
scheduler = BackgroundScheduler(timezone=JST)
scheduler.start()

app = Flask(__name__)

TIME_PATTERN_JP = re.compile(r"(?P<hour>[01]?\d|2[0-3])時(?:(?P<minute>[0-5]?\d)分)?")
TIME_PATTERN_COLON = re.compile(r"(?P<hour>[01]?\d|2[0-3]):(?P<minute>[0-5]\d)")


def build_reminder_time(hour: int, minute: int, now: Optional[datetime] = None) -> datetime:
    """指定の時間が過ぎていたら翌日に回して返す。"""
    now = now or datetime.now(JST)
    reminder = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if reminder <= now:
        reminder += timedelta(days=1)
    return reminder


def extract_time_and_task(message: str) -> Optional[Tuple[datetime, str]]:
    """「◯時◯分／◯:◯◯」のパターンを見つけてリマインド時間とタスク名を返す。"""
    match = TIME_PATTERN_JP.search(message)
    if match:
        hour = int(match.group("hour"))
        minute = int(match.group("minute") or 0)
        rest = message[match.end():]
    else:
        match = TIME_PATTERN_COLON.search(message)
        if not match:
            return None
        hour = int(match.group("hour"))
        minute = int(match.group("minute"))
        rest = message[match.end():]

    reminder_time = build_reminder_time(hour, minute)
    task = rest.lstrip(" 　,、。をにはがをってする！!?.")
    if not task:
        task = "宿題をやる"

    return reminder_time, task


def send_reminder(user_id: str, reminder_text: str) -> None:
    """ユーザーにリマインドメッセージを送信。"""
    line_bot_api.push_message(user_id, TextSendMessage(text=reminder_text))


@app.route("/health", methods=["GET"])
def health() -> tuple[str, int]:
    return "ok", 200


@app.route("/callback", methods=["POST"])
def callback() -> tuple[str, int]:
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400, description="Invalid signature.")

    return "OK", 200


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event: MessageEvent) -> None:
    user_message = event.message.text.strip()

    parsed = extract_time_and_task(user_message)

    if parsed:
        remind_at, task = parsed
        reminder_text = f"{remind_at.strftime('%H:%M')} になりました。「{task}」の時間です。"
        job_id = f"reminder-{event.source.user_id}"
        scheduler.add_job(
            send_reminder,
            "date",
            run_date=remind_at,
            args=[event.source.user_id, reminder_text],
            id=job_id,
            replace_existing=True,
        )
        reply = TextSendMessage(
            text=f"了解！{remind_at.strftime('%m/%d %H:%M')} に「{task}」をリマインドするね。"
        )
    else:
        reply = TextSendMessage(text="例: 10時に宿題をやる / 15:30に散歩 のように送ってね。")

    line_bot_api.reply_message(event.reply_token, reply)


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    app.run(host="0.0.0.0", port=port, debug=True)

