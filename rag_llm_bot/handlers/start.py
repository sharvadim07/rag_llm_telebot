from telegram import Update, constants
from telegram.ext import ContextTypes

from rag_llm_bot import db, message_texts


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user:
        raise ValueError("update.effective_user is None")
    if not update.message:
        raise ValueError("update.message is None")
    if not update.effective_chat:
        raise ValueError("update.effective_chat is None")
    # Set group chat as user if message send from it
    telegram_user_id = update.effective_user.id
    if update.effective_chat.type in (
        constants.ChatType.GROUP,
        constants.ChatType.SUPERGROUP,
    ):
        telegram_user_id = update.effective_chat.id
    try:
        await db.get_add_bot_user(telegram_user_id)
    except ValueError as e:
        raise ValueError(e)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message_texts.GREETNGS.format(username=update.effective_user.username),
        disable_notification=True,
    )
