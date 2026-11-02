# Telegram user-tag bot

A Telethon-based Telegram userbot. Use only in chats where you have permission to send automated messages and respect Telegram rate limits.

## Setup

1. Install Python and run `pip install -r requirements.txt`.
2. Set `API_ID`, `API_HASH`, and `SESSION` as environment variables in your terminal or deployment provider's secret manager.
3. To generate a session locally, set `API_ID` and `API_HASH` and run `PRINT_SESSION=1 python session_gen.py`. Keep the output secret.
4. Run `python new_utagbot.py`.

## Security

- Never commit `.env`, `*.session`, or a Telethon StringSession.
- Previously committed API credentials must be considered exposed even after removing them from the current file. Review account sessions and rotate/revoke credentials where supported.
- Removing a secret from a new commit does **not** remove it from Git history.
- The owner ID is currently configured in the bot source; adjust it only if you are the account owner.
