import asyncio
import re
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ================== ڕێکخستنەکان ==================
API_ID = 33790522
API_HASH = "00e4131295f55452e143c06099c1ddae"

# ✅ سێشنی نوێ
SESSION_STRING = "1ApWapzMBuzLx_9y2ZWfy_kMhzJuL4YaLOAC3rXUMWZbOKn9aZkNsGdnPug6mhUEHlfYltI6hUyzbA7pqOowRUJ5K4owWRJFs_B6HCLPhnOIwQTyhRcIlf1jDjcoUrG9D3jK41QvWlnnbY5AfROuU1mH1-ZJcaElJ89mH_xgPd3ujtHxPI8fhnfIVal4ixmcaqJ6XRLJ4FDwAAb6WhZWwI_NYXt486IF4VUA2lbsfPbvd2CD2ReGyd-gk657D-Wv_caipdnkqtK8guoumz85xWnZrt4W7Mbr9xlZJHiaXbAuD2cs74Vm2KLp7vINItaP0MuP1UwpsyQY1TPvKu1bEAHxMd-Yky_U="

SOURCE_CHANNEL = "@kroabscrap"
TARGET_CHANNEL = "@Kurdstan822"
# ====================================================

# ===== Regex ـەکان یەک جار کۆمپایل بکە (خێراترە) =====
RE_STAR      = re.compile(r'\*+')
RE_BACKTICK  = re.compile(r'`')
RE_TAKEN     = re.compile(r'Taken\s*[:➡\-]?\s*[\d.]+')
RE_TIME      = re.compile(r'Time\s*[:]?\s*[\d:]+')
RE_DEV       = re.compile(r'dev\s*@[\w.\-]+[^\n]*', re.IGNORECASE)
RE_HSPACE    = re.compile(r'[ \t]+')
RE_BLANKLINE = re.compile(r'\n\s*\n+')

def clean_text(text: str) -> str:
    text = RE_STAR.sub('', text)
    text = RE_BACKTICK.sub('', text)
    text = RE_TAKEN.sub('', text)
    text = RE_TIME.sub('', text)
    text = RE_DEV.sub('', text)
    text = RE_HSPACE.sub(' ', text)
    text = RE_BLANKLINE.sub('\n', text)
    return text.strip()

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    try:
        msg = event.message
        original_text = msg.text or ""
        cleaned_text = clean_text(original_text)

        if not cleaned_text:
            if msg.media:
                await client.send_file(
                    TARGET_CHANNEL,
                    msg.media,
                    caption="",
                )
                print("📎 میدیا نێردرا (بێ دەق)")
            else:
                print("⏭️ پەیام بەتاڵ بوو، فڕێدرا")
            return

        if msg.media:
            await client.send_file(
                TARGET_CHANNEL,
                msg.media,
                caption=cleaned_text,
            )
            print("✅ میدیا + دەق نێردرا")
        else:
            await client.send_message(TARGET_CHANNEL, cleaned_text)
            print("✅ پەیام نێردرا (دوای پاککردنەوە)")

    except Exception as e:
        print(f"❌ هەڵە: {type(e).__name__}: {e}")

async def main():
    await client.start()
    me = await client.get_me()
    print(f"🚀 بۆت کاردەکات وەک: {me.first_name} (@{me.username})")
    print(f"📡 سەرچاوە: {SOURCE_CHANNEL}")
    print(f"🎯 ئامانج: {TARGET_CHANNEL}")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
