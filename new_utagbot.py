from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantsAdmins
import asyncio
import random
import os
from datetime import datetime, timedelta, timezone

print("🚀 STARTING BOT...")

# 🔐 ENV
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")

OWNER_ID = 2025167583

client = TelegramClient("./session", api_id, api_hash)

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
        "🌚 utag qilganim uchun nechta almas berasiz?",
        "🎮 o‘yin boshlanyapti join bo‘ling",
        "👀 tez kelsayz almas beraman",
        "🌚 mandarinni po‘chog‘i",
        "😡 kelmasayz tepaman",

        # 🔥 YANGI KULGILI
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

# 🔒 OWNER CHECK
def is_owner(event):
    return event.sender_id == OWNER_ID

# ▶️ START
@client.on(events.NewMessage(pattern="\\.r"))
async def start(event):
    global running
    if not is_owner(event):
        return

    running = True

    try:
        await event.delete()
    except:
        pass

    chat = await event.get_chat()

    # 👮 ADMINLAR
    admins = []
    async for user in client.iter_participants(chat, filter=ChannelParticipantsAdmins):
        admins.append(user.id)

    me = await client.get_me()
    admins.append(me.id)

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

    active_users = list(active_users)
    fallback_users = list(fallback_users)

    print(f"🔥 Active: {len(active_users)} | Fallback: {len(fallback_users)}")

    used_users = set()
    count = 0
    LIMIT = 30

    while running and count < LIMIT:
        if active_users:
            user_id = random.choice(active_users)
        elif fallback_users:
            user_id = random.choice(fallback_users)
        else:
            print("⚠️ Userlar tugadi")
            break

        if user_id in used_users:
            continue

        used_users.add(user_id)

        try:
            user = await client.get_entity(user_id)

            await client.send_message(
                chat,
                f"[{user.first_name}](tg://user?id={user.id}) {get_ai_text()}"
            )

            count += 1
        except Exception as e:
            print("❌ Xatolik:", e)

        await asyncio.sleep(random.uniform(1.0, 1.5))

    running = False
    print("✅ Tugadi")

# ⏹ STOP
@client.on(events.NewMessage(pattern="\\.t"))
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

client.start()
client.run_until_disconnected()
