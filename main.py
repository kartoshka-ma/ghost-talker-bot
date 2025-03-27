from aiogram import Dispatcher, Bot, types
from aiogram.utils import executor
from dotenv import load_dotenv
from database import Database
import os
import asyncio

load_dotenv()
bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start_command(message: types.Message) -> None:
    msg = (
        "🇬🇧: *Welcome to the bot! 🎉 Type a message, "
        "and I'll deliver it anonymously.* 💬👻\n"
        "To get your unique link, just type /link. "
        "Share it if you want to get anonymous messages.\n\n"
        "🇷🇺: *Добро пожаловать в бота! 🎉"
        "Напишите сообщение, и я отправлю его анонимно.* 💬👻\n"
        "Чтобы получить вашу уникальную ссылку, просто напишите /link. "
        "Поделитесь ею, если хотите получать анонимные сообщения."
    )

    user_id = message.from_user.id
    recipient_id = message.get_args()

    if recipient_id:
        data = (user_id, int(recipient_id))
        async with Database(os.getenv("DATABASE_URL")) as db:
            await db.insert_data(data)

    await message.reply(text=msg, parse_mode="Markdown")

@dp.message_handler(commands="link")
async def create_link(message: types.Message) -> None:
    user_id = message.from_user.id
    link = f"t.me/GhostTalkerrBot?start={user_id}"
    msg = (
        f"🇬🇧: *Here is your unique link:* {link}\n"
        "*If you want to receive anonymous messages, make sure to share your link.*\n\n"
        f"🇷🇺: *Вот ваша уникальная ссылка:* {link}\n"
        "*Если хотите получать анонимные сообщения, не забудьте поделиться своей ссылкой.*"
    )

    await message.reply(msg, parse_mode="Markdown")

@dp.message_handler()
async def echo_message(message: types.Message) -> None:
    user_id = message.from_user.id
    async with Database(os.getenv("DATABASE_URL")) as db:
        data = await db.connection.fetch("SELECT recipient_id FROM users WHERE user_id = $1 LIMIT 1", user_id)

    if data:
        msg = (
            "🇬🇧: *New anonymous message received!* 💌👀\n"
            "🇷🇺: *Получено новое анонимное сообщение!* 💌👀\n"
            "────────────────────\n"
            "📝 *Message / Сообщение:*\n"
            f"{message.text}"
        )
        await bot.send_message(data[0]["recipient_id"], msg, parse_mode="Markdown")
    else:
        await message.reply("🇬🇧: User not found\n🇷🇺: Пользователь не найден")

async def main():
    print("Bot is running...")
    async with Database(os.getenv("DATABASE_URL")) as db:
        await db.create_table()
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
