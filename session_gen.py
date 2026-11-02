"""Generate a Telethon StringSession using credentials from environment variables.

Never commit or share the printed session string.
"""
import os
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id_raw = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
if not api_id_raw or not api_id_raw.isdigit() or not api_hash:
    raise SystemExit("Set API_ID (numeric) and API_HASH environment variables first.")

with TelegramClient(StringSession(), int(api_id_raw), api_hash) as client:
    session = client.session.save()
    print("Session created. Treat this as a password; do not paste it into GitHub or chat.")
    if os.getenv("PRINT_SESSION") == "1":
        print(session)
    else:
        print("To display it locally, rerun with PRINT_SESSION=1.")
