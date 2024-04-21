import logging

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from rag_llm_bot import handlers
from rag_llm_bot.config import config

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def main():
    application = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()

    # Add the handlers to the dispatcher
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.text_message)
    )
    start_handler = CommandHandler("start", handlers.start)
    application.add_handler(start_handler)

    application.run_polling()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # import traceback

        # logging.warning(traceback.format_exc())
        logging.warning(e)
    finally:
        logging.info("Bot stopped.")
