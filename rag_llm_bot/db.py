from collections import OrderedDict
from dataclasses import dataclass
from typing import Optional

import aiosqlite

from rag_llm_bot.config import config


@dataclass
class DataText:
    data_text_id: int
    created_at: str
    content: Optional[str]


"""
    data_id INT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMPNOT NOT NULL,
    telegram_user_id INT NOT NULL,
    FOREIGN KEY (telegram_user_id) REFERENCES user (telegram_user_id)
"""


@dataclass
class BotUser:
    telegram_user_id: int
    created_at: str
    data_texts: Optional[OrderedDict[int, DataText]]


"""
    telegram_user_id BIGINT PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
"""


async def add_new_bot_user_db(telegram_user_id: int) -> Optional[BotUser]:
    bot_user = None
    async with aiosqlite.connect(config.SQLITE_DB_FILE) as db:
        db.row_factory = aiosqlite.Row
        await db.execute(
            f"""
            INSERT INTO bot_user (telegram_user_id)
            VALUES ({telegram_user_id});
            """
        )
        await db.commit()
        async with db.execute(
            f"""
            SELECT *
              FROM bot_user
             WHERE telegram_user_id = {telegram_user_id};
            """
        ) as cursor:
            async for row in cursor:
                bot_user = BotUser(row["telegram_user_id"], row["created_at"], None)
    return bot_user


async def get_bot_user_db(telegram_user_id: int) -> Optional[BotUser]:
    bot_user = None
    async with aiosqlite.connect(config.SQLITE_DB_FILE) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            f"""
            SELECT *,
                   bot_user.created_at AS bot_user_created_at,
                   data_text.created_at AS data_text_created_at
              FROM bot_user
              LEFT JOIN data_text USING(telegram_user_id)
             WHERE telegram_user_id = {telegram_user_id}
             ORDER BY data_text.created_at DESC;
            """
        ) as cursor:
            async for row in cursor:
                if row["data_text_id"] is not None:
                    if not bot_user:
                        bot_user = BotUser(
                            row["telegram_user_id"],
                            row["bot_user_created_at"],
                            OrderedDict(
                                {
                                    row["data_text_id"]: DataText(
                                        row["data_text_id"],
                                        row["data_text_created_at"],
                                        row["content"],
                                    )
                                }
                            ),
                        )
                    else:
                        bot_user.data_texts[row["data_text_id"]] = DataText(
                            row["data_text_id"],
                            row["data_text_created_at"],
                            row["content"],
                        )
                else:
                    bot_user = BotUser(row["telegram_user_id"], row["created_at"], None)
    return bot_user


async def get_add_bot_user(telegram_user_id: int) -> BotUser:
    # Get user from DB
    bot_user = await get_bot_user_db(telegram_user_id)
    if not bot_user:
        bot_user = await add_new_bot_user_db(telegram_user_id)
    if not bot_user:
        raise ValueError("bot_user is None")
    return bot_user
