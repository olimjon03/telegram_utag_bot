from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantsAdmins
from telethon.sessions import StringSession
from telethon.errors import FloodWaitError
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

client = TelegramClient(
    StringSession(session_str),
    api_id,
    api_hash,
    auto_reconnect=True,
    connection_retries=None
)

running = False

# 😂 RANDOM TEXT (o‘zgarmagan)
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
        "🌚 utag qilganim uchun nechta almas berasiz?",
        "🎮 o‘yin boshlanyapti join bo‘ling",
        "👀 tez kelsayz almas beraman",
        "🌚 mandarinni po‘chog‘i",
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
        "😂 ketib qolyapsizmi yoq qochib qolyapsizmi",
        "😅 hozir kelmasayz ban 😜",
        "👀 sirli o‘yin boshlandi",
        "💀 kech qolsangiz pushaymon bo‘lasiz",
        "😏 sizsiz boshlamaymiz",
        "🤣 qochma baribir topamiz",
        "👀 sizni kuzatib turibmiz",
        "😈 bugun sizga omad yo‘q shekilli",
        "🔥 tez keling drama bor",
        "🥸 maxfiy chaqiruv",
        "😜 kelmasayz screenshot bor",
        "👀 sizni tag qilishdi, reaction qani",
        "😂 telefonni tashlab qochmang",
        "😎 bu imkoniyat faqat siz uchun",
        "💣 hozir boshlanadi tayyor turing",
    ])

def is_owner(event):
    return event.sender_id == OWNER_ID

# ▶️ START
@client.on(events.NewMessage(pattern=r"\.r"))
async def start(event):
    global running

    if not is_owner(event) or running:
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

    # ⏱ Aktiv userlar
    now = datetime.now(timezone.utc)
    five_min_ago = now - timedelta(minutes=20)

    active_users = set()
    fallback_users = set()

    async for msg in client.iter_messages(chat, limit=4000):
        if not msg.sender_id or msg.sender_id in admins:
            continue

        if msg.date and msg.date >= five_min_ago:
            active_users.add(msg.sender_id)
        else:
            fallback_users.add(msg.sender_id)

    users_pool = list(active_users) if active_users else list(fallback_users)

    if not users_pool:
        print("⚠️ User yo‘q")
        running = False
        return

    random.shuffle(users_pool)

    # 🔥 20–40 USER
    LIMIT = min(random.randint(20, 40), len(users_pool))

    print(f"🔥 Start | {LIMIT} ta user")

    for i, user_id in enumerate(users_pool[:LIMIT]):

        if not running:
            break

        try:
            user = await client.get_entity(user_id)
            name = user.first_name or "User"

            await client.send_message(
                chat,
                f"[{name}](tg://user?id={user.id}) {get_ai_text()}",
                parse_mode="md"
            )

            print(f"✅ {name}")

            # ⚡ TEZLIK
            await asyncio.sleep(random.uniform(1.5 , 2.5))

            # 😴 HAR 10 USERDAN KEYIN (MAX 10s)
            if i % 10 == 9:
                pause = random.uniform(6, 10)
                print(f"😴 Pause {pause:.1f}s")
                await asyncio.sleep(pause)

        except FloodWaitError as e:
            print(f"⏳ Flood: {e.seconds}s kutamiz")
            await asyncio.sleep(e.seconds + 5)

        except Exception as e:
            print("❌ Xato:", e)
            await asyncio.sleep(2)

    running = False
    print("✅ Tugadi")

# ⏹ STOP
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
