import requests
import bs4
import urllib.parse

from fake_useragent import UserAgent


def parse(search_book: str) -> list:
    url = f"https://www.yakaboo.ua/ua/search/?multi=0&cat=&q={urllib.parse.quote_plus(search_book)}"
    answer_site = create_sessions(url)
    get_page = get_information(answer_site)
    try:
        result_firs_site = list(map(parse_informations, get_page))
    except KeyError:
        result_firs_site = [url]
    except TypeError:
        result_firs_site = []
    if len(result_firs_site) == 1:
        return [result_firs_site[0]]
    elif len(result_firs_site) == 0:
        return ["На жаль, за вашим запитом нічого не знайдено."]
    else:
        return result_firs_site[:10]


def create_sessions(url: str) -> requests.models.Response:
    headers = {"User-Agent": UserAgent().random}
    session = requests.Session()
    session.headers.update(headers)
    response = session.get(url, headers={"x-requested-with": "XMLHttpRequest"})
    return response


def get_information(site_response:requests.models.Response) -> list:
    soup = bs4.BeautifulSoup(site_response.text, "lxml")
    availability_book = soup.select_one(".note-msg")
    if isinstance(availability_book, bs4.element.Tag):
        news_block_list = availability_book.text.strip()
    else:
        news_block_list = soup.select(".product-name")

    return news_block_list


def parse_informations(html_page):
    return html_page["href"]
