import requests
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

API_URL = "https://tikdown.sl-bjs.workers.dev/?url="
TOKEN = "8125567952:AAHGg77fmzUjT1QNAGiQbxbVCvzcrE9WFto"  # Your BotFather Token

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📥 Send a TikTok link and I'll download the video and audio separately.\n\n"
        "#TikTokDownloader #PasinduBot"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if "tiktok.com" not in url:
        await update.message.reply_text("❌ Please send a valid TikTok URL.\n#InvalidLink")
        return

    await update.message.reply_text("⏳ Downloading video and audio...\n#TikTokDownloader")

    try:
        res = requests.get(API_URL + url, timeout=60)
        data = res.json()

        if not data.get("success"):
            await update.message.reply_text("⚠️ Failed to download. Please try another link.\n#DownloadFailed")
            return

        title = data.get("title", "TikTok Video")
        video_url = data.get("video_url")
        audio_url = data.get("audio_url")

        # --- Download & Send Video ---
        video_path = "video.mp4"
        with open(video_path, "wb") as f:
            f.write(requests.get(video_url, timeout=60).content)

        with open(video_path, "rb") as video_file:
            await update.message.reply_video(
                video=video_file,
                caption=f"🎬 {title}\n\n#TikTokVideo #Pasindu 🇱🇰\n📢 @sl_bjs"
            )
        os.remove(video_path)

        # --- Download & Send Audio ---
        if audio_url:
            audio_path = "audio.mp3"
            with open(audio_path, "wb") as f:
                f.write(requests.get(audio_url, timeout=60).content)

            with open(audio_path, "rb") as audio_file:
                await update.message.reply_audio(
                    audio=audio_file,
                    title=f"{title} - Audio",
                    caption=f"🎧 Audio Only\n\n#TikTokAudio #Pasindu 🇱🇰\n📢 @sl_bjs"
                )
            os.remove(audio_path)

    except requests.exceptions.Timeout:
        await update.message.reply_text("⏱️ Timeout while downloading. Please try again later.\n#Timeout")
    except Exception as e:
        await update.message.reply_text(f"❌ An error occurred:\n{e}\n#Error")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("🚀 Bot is running...")
    app.run_polling()
