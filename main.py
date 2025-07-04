from telethon import TelegramClient, events, Button
import os, json, datetime, requests
from collections import defaultdict

API_ID = 23988357  # ضع API ID هنا إذا كنت تريد إنشاء جلسة جديدة
API_HASH = '25bee10ac433f3dc16a2c0d78bb579de'  # ضع API HASH هنا إذا كنت تريد إنشاء جلسة جديدة

client = TelegramClient('my_session', API_ID, API_HASH).start()

FAST_API_URL = "http://sii3.moayman.top/api/gpt.php"
DEEP_API_URL = "https://sii3.moayman.top/api/black.php"

ADMIN_ID = 7216718830

user_states = defaultdict(lambda: {
    'mode': 'fast',
    'fast_model': 'searchgpt',
    'deep_model': 'blackbox'
})

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    user_id = event.sender_id
    user_states[user_id] = {'mode': 'fast', 'fast_model': 'searchgpt', 'deep_model': 'blackbox'}
    msg = "**أهلًا بك في بوت netro_gz**\n\nأرسل رسالتك أو ملف للمعالجة.\nالوضع الحالي: سريع"
    buttons = [[Button.url("netro_gz", "https://t.me/python_gaza")]]
    await event.respond(msg, buttons=buttons)

@client.on(events.NewMessage)
async def handler(event):
    user_id = event.sender_id
    if event.text.startswith('/'):
        return

    state = user_states[user_id]
    mode = state['mode']
    model = state['fast_model'] if mode == 'fast' else state['deep_model']
    prompt = event.text

    try:
        await event.respond("⏳ استنا قاعد بفكر")
        if mode == 'fast':
            response = requests.get(FAST_API_URL, params={model: prompt}, timeout=60).json()
            reply = response.get("reply", "❌ مش ملاقي رد مناسب")
        else:
            response = requests.post(DEEP_API_URL, data={model: prompt}, timeout=90).json()
            reply = response.get("response", "❌ ماعندي رد مناسب")
        await event.respond(reply)
    except Exception as e:
        await event.respond(f"حدث خطأ: {e}")

client.start()
print("اشتغل السورس..")
client.run_until_disconnected()
