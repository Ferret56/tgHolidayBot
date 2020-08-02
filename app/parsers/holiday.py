from bs4 import BeautifulSoup


class HolidayParser:
    @staticmethod
    def parse_holidays_country_page(holidays_page_html: str) -> dict:
        """
        :param holidays_page_html - html страница с праздниками по стране
        :return: словарь 'дата' -> 'праздник'
        """
        li_tags = HolidayParser.get_li_tags_by_country_html_page(holidays_page_html)
        holidays_dict = HolidayParser.parse_country_holidays_by_li_tags(li_tags)
        return holidays_dict

    @staticmethod
    def get_li_tags_by_country_html_page(holidays_page_html: str):
        """
        :param holidays_page_html - html страница с праздниками по стране
        :return: все теги <li> с описанием праздников
        """
        soup = BeautifulSoup(holidays_page_html, 'lxml')
        # Список со всеми гос. праздниками в стране
        ul_tag = soup.find('ul', {'class': 'itemsNet'})
        li_tags = ul_tag.find_all('li', {'class': 'full'})
        return li_tags

    @staticmethod
    def parse_country_holidays_by_li_tags(li_tags):
        """
        :param li_tags: все теги <li> с описанием праздников
        :return: словарь 'дата' -> 'праздник'
        """
        holidays_dict = {}
        for li in li_tags:
            # Блок даты
            span_date = li.find('span', {'class': 'dataNum'})
            # Блок празднника
            span_caption = li.find('span', {'class': 'caption'})

            holiday_date = HolidayParser.parse_date(span_date)

            holiday_date_full = HolidayParser.parse_date_full(span_date)

            holiday_title = HolidayParser.parse_title(span_caption)

            holidays_dict.update(
                {
                    holiday_date:
                        {
                         'date': holiday_date_full,
                         'title': holiday_title
                        }
                 }
            )
        return holidays_dict

    @staticmethod
    def parse_date(span_date) -> str:
        """
        :param span_date: блок <span> c датой праздника
        :return: дата праздника в формате 'гггг-м-д'
        """
        holiday_date = span_date.find('a').attrs.get('href')
        holiday_date_without_slash = holiday_date.replace('/', '')
        holiday_date_clear = holiday_date_without_slash.replace('day', '')
        return holiday_date_clear

    @staticmethod
    def parse_date_full(span_date):
        """
        :param span_date: блок <span> c датой праздника
        :return: дата праздника в строковом формат, например '1 июля'
        """
        holiday_day = span_date \
            .find('a') \
            .find('span', {'class': 'number'}) \
            .text

        holiday_month = span_date \
            .find('a') \
            .find('span', {'class': 'desc'}) \
            .find('span', {'class': 'title'}) \
            .text
        return holiday_day + ' ' + holiday_month

    @staticmethod
    def parse_title(span_caption) -> str:
        """
        :param span_caption: блок <span>
        :return: название праздника
        """
        holiday_title = span_caption \
            .find('span', {'class': 'title'}) \
            .find('a') \
            .text
        return holiday_title
