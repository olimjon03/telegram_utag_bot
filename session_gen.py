from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = 37433100
api_hash = "9af57ef058fa1d3e994225ca423b8d17"

with TelegramClient(StringSession(), api_id, api_hash) as client:
    print("SESSION STRING:")
    print(client.session.save())