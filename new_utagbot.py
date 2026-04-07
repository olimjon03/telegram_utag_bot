from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantsAdmins
import asyncio
import random
import os

print("🚀 STARTING BOT...")

# 🔐 ENV (Railway Variables)
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")

# 👤 OWNER ID
OWNER_ID = 2025167583

# 🔥 MUHIM: session path to‘g‘rilandi
client = TelegramClient("./session", api_id, api_hash)

running = False

# 🔥 RANDOM TEXT
def get_ai_text():
    mafia_words = [
        "Mafia", "Boss", "Don", "O‘yin", "Kecha", "Jang",
        "Sir", "Qorong‘u", "Shahar", "Tungi o‘yin", "Agent", "Killer"
    ]

    actions = [
        "boshlanadi", "kutmoqda", "seni chaqiryapti", "qizib ketdi",
        "start oldi", "yashirin ketmoqda", "kuchaymoqda",
        "davom etyapti", "tayyor", "portlaydi"
    ]

    fun_words = [
        "😂", "😈", "🔥", "😎", "👀", "💣",
        "🎭", "🤣", "😜", "🕵️"
    ]

    phrases = [
        "tez qo‘shil", "qochma", "bugun omad sendami",
        "sen tanlanding", "kuzatyapmiz", "ushlab oldik",
        "navbat senda", "o‘yin kutyapti",
        "barchasi boshlanadi", "qiziq bo‘ladi",
        "oxirgi imkoniyat", "hamma kutyapti"
    ]

    templates = [
        "{emoji} {mafia} {action}",
        "{emoji} {phrase}",
        "{emoji} {mafia} {phrase}",
        "{emoji} {mafia} {action}, {phrase}",
        "{emoji} Bugun {mafia} {action}",
        "{emoji} {phrase}, {mafia} {action}",
    ]

    return random.choice(templates).format(
        emoji=random.choice(fun_words),
        mafia=random.choice(mafia_words),
        action=random.choice(actions),
        phrase=random.choice(phrases)
    )

# 🔒 OWNER CHECK
def is_owner(event):
    return event.sender_id == OWNER_ID

# ▶️ START (.r)
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

    # 🎯 ACTIVE USERLAR
    active_users = set()
    async for msg in client.iter_messages(chat, limit=150):
        if msg.sender_id and msg.sender_id not in admins:
            active_users.add(msg.sender_id)

    active_users = list(active_users)

    count = 0
    LIMIT = 30

    while running and count < LIMIT:
        if not active_users:
            break

        user_id = random.choice(active_users)

        try:
            user = await client.get_entity(user_id)
            text = get_ai_text()

            await client.send_message(
                chat,
                f"[{user.first_name}](tg://user?id={user.id}) {text}"
            )

            count += 1
        except Exception as e:
            print("❌ Xatolik:", e)

        await asyncio.sleep(random.uniform(1.0, 1.5))

    running = False

# ⏹️ STOP (.t)
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

# 🚀 RUN
print("✅ Bot ishga tushdi...")

client.start()
client.run_until_disconnected()
