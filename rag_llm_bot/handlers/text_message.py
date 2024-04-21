from typing import Dict

from telegram import Update, constants
from telegram.ext import ContextTypes

# from rag_llm_bot import message_texts


async def text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Function to handle the button selection and text input"""
    if not update.message:
        raise ValueError("update.callback_query is None")
    if not update.message.text:
        raise ValueError("update.message.text is None")
    if not update.effective_user:
        raise ValueError("update.effective_user is None")
    if not isinstance(context.chat_data, Dict):
        raise ValueError("context.chat_data is None")
    if not update.effective_chat:
        raise ValueError("update.effective_chat is None")
    # Set group chat as user if message send from it
    telegram_user_id = update.effective_user.id
    if update.effective_chat.type in (
        constants.ChatType.GROUP,
        constants.ChatType.SUPERGROUP,
    ):
        telegram_user_id = update.effective_chat.id
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Your userif is {telegram_user_id}.\nYour message is {update.message}",
        disable_notification=True,
    )
