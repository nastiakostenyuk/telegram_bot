from aiogram import Bot, Dispatcher, executor, types
from parse import parse

API_TOKEN = 'token'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start(message: types.Message):
    await message.reply("Привіт! Введи назву книги, яку хочеш знайти на просторах інтернету :)")


@dp.message_handler()
async def process_start(message: types.Message):
    result_parse = parse(message.text)
    for element in result_parse:
        await message.reply(element)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
