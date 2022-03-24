import logging
import parse2

from aiogram import Bot, Dispatcher, executor, types


logging.basicConfig(level=logging.INFO)

API_TOKEN = '5002816244:AAFaHn6rEzLX_lSsJ0Nj6kQb06jMTbBGmaY'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start(message: types.Message):
    await message.reply("Привіт! Введи назву книги, яку хочеш знайти на просторах інтернету :)")


@dp.message_handler()
async def process_start(message: types.Message):
    first_site = parse2.Yakaboo(message.text)
    answer = first_site.create_sessions()
    get_page = first_site.get_html(answer)
    try:
        result_firs_site = list(map(first_site.parse_informations, get_page))
    except KeyError:
        result_firs_site = [first_site.link]
    except TypeError:
        result_firs_site = []
    if len(result_firs_site) == 1:
        await message.reply(result_firs_site[0])
    elif len(result_firs_site) == 0:
        await message.reply("На жаль, за вашим запитом нічого не знайдено.")
    else:
        for element in result_firs_site[:10]:
            await message.reply(element)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)