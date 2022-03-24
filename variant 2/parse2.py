import requests
import bs4
import urllib.parse


from fake_useragent import UserAgent


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

    def parse_information(self, html_page):
        return html_page["href"]
