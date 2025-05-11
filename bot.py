import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import instaloader

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

loader = instaloader.Instaloader()

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome! Send me an Instagram Reel link to download it.')

def handle_message(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    if 'instagram.com/reel/' in url:
        try:
            shortcode = url.split('/')[-2]

            target_dir = 'downloads'
            os.makedirs(target_dir, exist_ok=True)

            # Download the post to target_dir
            loader.download_post(instaloader.Post.from_shortcode(loader.context, shortcode), target=target_dir)

            video_path = os.path.join(target_dir, shortcode + '.mp4')
            if os.path.exists(video_path):
                with open(video_path, 'rb') as video:
                    update.message.reply_video(video)
            else:
                update.message.reply_text("Sorry, couldn't find the video file after download.")
        except Exception as e:
            logger.error(f"Error downloading reel: {e}")
            update.message.reply_text(f'Error: {str(e)}')
    else:
        update.message.reply_text('Please send a valid Instagram Reel link.')

def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable not set.")
        exit(1)

    updater = Updater(token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
  
