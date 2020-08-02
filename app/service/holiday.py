from app.utils.country_mapper import mapper
import datetime
from app.requests.holiday import HolidayRequests
from app.parsers.holiday import HolidayParser


class CountryNotFoundException(Exception):
    def __init__(self, message):
        self.message = message


class HolidayService:
    @staticmethod
    def get_current_holiday_in_country(country_cyrillic: str) -> dict:
        country_latin = mapper.get(country_cyrillic.lower())
        if not country_latin:
            raise CountryNotFoundException('Страна {} не найдена в каталоге'
                                           .format(country_cyrillic))

        today = datetime.date.today()
        today_str = '{}-{}-{}'.format(today.year, today.month, today.day)

        get_holiday_page_html = HolidayRequests.holidays_request_by_country(country_latin)
        holidays_dict = HolidayParser.parse_holidays_country_page(get_holiday_page_html)

        return holidays_dict.get(today_str)
