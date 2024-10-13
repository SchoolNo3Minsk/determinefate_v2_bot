import aiohttp

from typing import List, Optional

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from src.utils.models import Partizan, PartizanPerson, AllPartizans

PARAMS = {
    'Фамилия': 'surname',
    'Имя': 'name',
    'Отчество': 'middlename',
    'Дата рождения/Возраст': 'date_of_birth',
    'Место рождения': 'place_of_birth',
    'Дата и место призыва': 'call_place',
    'Последнее место службы': 'last_call_place',
    'Воинское звание': 'rank',
    'Причина выбытия': 'reason_of_leave',
    'Дата выбытия': 'date_of_leave',
    'Место выбытия': 'place_of_leave',
    'Название источника донесения': 'issue'
}

chrome_options = Options()
chrome_options.add_argument("headless")


class Parser:
    def __init__(self):
        self.base_url = "https://obd-memorial.ru"
        self.session = aiohttp.ClientSession(base_url=self.base_url)

        self.service = Service(executable_path="")
        self.browser = webdriver.Chrome(options=chrome_options, service=self.service)

    @staticmethod
    def _get_param_data(soup: BeautifulSoup, title: str) -> str | None:
        try:
            return soup.find('span', {'class': 'card_param-title'}, text=title).find_next_sibling('span').text
        except AttributeError:
            return None

    async def get_partizans_query(
            self,
            surname: Optional[str] = None,
            name: Optional[str] = None,
            middlename: Optional[str] = None,
            year_of_birth: Optional[int] = None,
            rank: Optional[str] = None,
            page: Optional[int] = 1,
    ):
        link = self.base_url + f"/html/search.htm?f={surname}&n={name}&s={middlename}&y={year_of_birth}&r={rank}&p={page}"

        self.browser.get(link.replace("None", ""))
        self.browser.implicitly_wait(1.5)

        div_elements = self.browser.find_elements('tag name', 'div')

        results: List = []

        for div in div_elements:
            if div.get_attribute('id'):
                _id = div.get_attribute('id')

                if _id.isdigit():
                    full_name = div.find_element(
                        by="css selector",
                        value="div:nth-child(3) > div:nth-child(1) > div:nth-child(1)"
                    ).text

                    date_of_birth = div.find_element(
                        by="css selector",
                        value="div:nth-child(3) > div:nth-child(1) > div:nth-child(2)"
                    ).text

                    date_of_die = div.find_element(
                        by="css selector",
                        value="div:nth-child(3) > div:nth-child(1) > div:nth-child(3)"
                    ).text

                    results.append(
                        {
                            "id": _id,
                            "full_name": full_name,
                            "date_of_birth": date_of_birth,
                            "date_of_die": date_of_die
                        }
                    )

        if len(results) == 0:
            return None

        return AllPartizans(Partizan(**data) for data in results) if results else None

    async def get_partizan(self, patrizan_id: int):
        async with self.session as session:
            async with session.get(f"/html/info.htm?id={patrizan_id}") as response:
                text = await response.text()

                soup = BeautifulSoup(text, features='lxml')
                data = {key: self._get_param_data(soup, title) for title, key in PARAMS.items()}

                return PartizanPerson(**data)


api = Parser()
