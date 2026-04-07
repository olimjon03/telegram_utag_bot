from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.sessions import StringSession
import asyncio
import random
import os
from datetime import datetime, timedelta, timezone

print("🚀 STARTING BOT...")

# 🔐 ENV
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
session_str = os.environ.get("SESSION")

OWNER_ID = 2025167583

# ✅ CLIENT (Railway uchun optimal)
client = TelegramClient(
    StringSession(session_str),
    api_id,
    api_hash,
    auto_reconnect=True,
    connection_retries=None
)

running = False

# 😂 RANDOM TEXT
def get_ai_text():
    return random.choice([
        "🔥 o‘yin boshlanadi",
        "😈 sen tanlanding",
        "😂 qochma",
        "👀 kuzatyapmiz",
        "💣 bugun qiziq bo‘ladi",
        "🌚 snikers olib berimi",
        "👀 bittasi chaqiryapti sizni",
        "🥸 byax kelingchi tez",
        "😕 nima ish qilib qo‘ydiz",
        "😅 chuchvara yeysizmi",
        "👀 Tojiboev sizni chaqiryapti",
        "🎮 o‘yin boshlanyapti join bo‘ling",
        "👀 tez kelsayz almas beraman",
        "😡 kelmasayz tepaman",
        "🤣 admin ko‘ryapti tez yoz",
        "😳 bu yerda nima gap bo‘lyapti",
        "👀 sizni qidirishyapti",
        "😂 yashirinish befoyda",
        "😈 bugun siz navbatdasiz",
        "🔥 gap bor tez keling",
        "🥲 kelmasayz xafa bo‘laman",
        "😎 VIP mehmon keldi",
        "🤨 sizni kimdir eslayapti",
        "👻 ruhlar sizni chaqiryapti",
        "😅 hozir kelmasayz ban 😜",
        "💀 kech qolsangiz pushaymon bo‘lasiz",
        "😏 sizsiz boshlamaymiz",
        "🤣 qochma baribir topamiz",
        "👀 sizni kuzatib turibmiz",
        "🔥 tez keling drama bor",
        "🥸 maxfiy chaqiruv",
    ])

# 🔒 OWNER CHECK
def is_owner(event):
    return event.sender_id == OWNER_ID

# ▶️ START (.r)
@client.on(events.NewMessage(pattern=r"\.r"))
async def start(event):
    global running

    if not is_owner(event):
        return

    if running:
        return

    running = True

    try:
        await event.delete()
    except:
        pass

    chat = await event.get_chat()

    # 👮 ADMINLAR
    admins = set()
    async for user in client.iter_participants(chat, filter=ChannelParticipantsAdmins):
        admins.add(user.id)

    me = await client.get_me()
    admins.add(me.id)

    # ⏱ 5 minut
    now = datetime.now(timezone.utc)
    five_min_ago = now - timedelta(minutes=5)

    active_users = set()
    fallback_users = set()

    async for msg in client.iter_messages(chat, limit=500):
        if not msg.date or not msg.sender_id:
            continue

        if msg.sender_id in admins:
            continue

        if msg.date >= five_min_ago:
            active_users.add(msg.sender_id)
        else:
            fallback_users.add(msg.sender_id)

    users_pool = list(active_users) if active_users else list(fallback_users)

    if not users_pool:
        print("⚠️ Userlar topilmadi")
        running = False
        return

    random.shuffle(users_pool)

    LIMIT = min(30, len(users_pool))

    print(f"🔥 Ishlayapti | {LIMIT} ta user")

    for i in range(LIMIT):
        if not running:
            break

        user_id = users_pool[i]

        try:
            user = await client.get_entity(user_id)
            name = user.first_name or "User"

            await client.send_message(
                chat,
                f"[{name}](tg://user?id={user.id}) {get_ai_text()}",
                parse_mode="md"
            )

        except Exception as e:
            print("❌ Xatolik:", e)

        await asyncio.sleep(random.uniform(1.0, 1.5))

    running = False
    print("✅ Tugadi")

# ⏹ STOP (.t)
@client.on(events.NewMessage(pattern=r"\.t"))
async def stop(event):
    global running

    if not is_owner(event):
        return

    running = False

    try:
        await event.delete()
    except:
        pass

print("✅ Bot ishga tushdi...")

# 🚀 RUN
async def main():
    await client.start()
    await client.run_until_disconnected()

asyncio.run(main())
