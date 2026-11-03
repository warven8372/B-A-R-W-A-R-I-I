import asyncio
import re
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ================== ڕێکخستنەکان ==================
API_ID = 33790522
API_HASH = "00e4131295f55452e143c06099c1ddae"

# ✅ سێشنی نوێ لێرە دانراوە
SESSION_STRING = "1ApWapzMBu0UVGwoi0wVdubb9DChXtMDut3_Y9ojBrl6wjlggvnZXHhoUrQqsBZBnGu3uh1WvEObhf1gQeQZyRbeXISzt6FwXrWvXhnpwwN-MA0tXQ81uXdUNWIvqM6EBUBdvjMVEsMpix4ykeA0GToGQCLnSv1Ude5xE27usi3TCTXpaFxX6yhxpjArNHJAztU4oWQXE1egEeWGGegIIrpkG73kSx6vaNyzQp-vpwEw1-s6Y8gdYX-L7_Q_aEu8KiJN4IMhdkzbD71ywu2OG2IL3g9TI5Mlniu1XD6iAYSR-6SHk4GjigLJNw2Jg2ab0qnyTuVQ-FTo0C1Py95huRKINx4zD8SY="

SOURCE_CHANNEL = "@kroabscrap"
TARGET_CHANNEL = "@duhok_KRD"
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
    """
    تەنها ئەم شتانە لادەبات:
    - ستێرە (*) و بەک‌تیک (`)
    - واتەرمارک: "Taken ➡ 12.592312"
    - هێڵی کات: "Time 10:00:00"
    - ناوی پەرەپێدەر: "dev @warven_24 💻"
    - بۆشایی زیادە (بەڵام newline دەپارێزێت)
    """
    text = RE_STAR.sub('', text)
    text = RE_BACKTICK.sub('', text)
    text = RE_TAKEN.sub('', text)
    text = RE_TIME.sub('', text)
    text = RE_DEV.sub('', text)
    text = RE_HSPACE.sub(' ', text)        # ✅ تەنها space/tab
    text = RE_BLANKLINE.sub('\n', text)    # ✅ هێڵی بەتاڵ بسڕەرەوە
    return text.strip()

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHANNEL))
async def handler(event):
    try:
        msg = event.message
        original_text = msg.text or ""
        cleaned_text = clean_text(original_text)

        # ✅ ئەگەر دەق نییە بەڵام میدیا هەیە → میدیاکە بنێرە
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

        # ✅ ئەگەر میدیا هەبوو لەگەڵ کاپشنەکە بینێرە
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
