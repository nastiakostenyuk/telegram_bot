import requests
import bs4
import urllib.parse


from fake_useragent import UserAgent
from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = 'token'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start(message: types.Message):
    await message.reply("Привіт! Введи назву книги, яку хочеш знайти на просторах інтернету :)")


@dp.message_handler()
async def process_start(message: types.Message):
    first_site = Yakaboo(message.text)
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


class Yakaboo:

    def __init__(self, search_book):
        self.url = "https://www.yakaboo.ua/ua/search/?multi=0&cat=&q="
        self.link = f"{self.url}{urllib.parse.quote_plus(search_book)}"

    def create_sessions(self) -> requests.models.Response:
        headers = {"User-Agent": UserAgent().random}
        session = requests.Session()
        session.headers.update(headers)
        response = session.get(self.link, headers={"x-requested-with": "XMLHttpRequest"})
        return response

    def get_html(self, site_response: requests.models.Response) -> list:
        soup = bs4.BeautifulSoup(site_response.text, "lxml")
        availability_book = soup.select_one(".note-msg")
        if isinstance(availability_book, bs4.element.Tag):
            news_block_list = availability_book.text.strip()
        else:
            news_block_list = soup.select(".product-name")
        return news_block_list

    def parse_informations(self, html_page):
        return html_page["href"]


class LavkaBabuin:
    pass


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
