from app.utils.country_mapper import mapper
import datetime
from app.requests.holiday import HolidayRequests
from app.parsers.holiday import HolidayParser


class CountryNotFoundException(Exception):
    def __init__(self, message):
        self.message = message


class HolidayNotFoundException(Exception):
    def __init__(self, message=None):
        self.message = message


class HolidayService:
    @staticmethod
    def get_current_holiday_in_country(country_cyrillic: str) -> dict:
        country_latin = mapper.get(country_cyrillic.lower())
        if not country_latin:
            raise CountryNotFoundException('Страна {} не найдена в каталоге'
                                           .format(country_cyrillic))

        get_holiday_page_html = HolidayRequests.holidays_request_by_country(country_latin)
        holidays_dict = HolidayParser.parse_holidays_country_page(get_holiday_page_html)

        today = datetime.date.today()
        today_str = '{}-{}-{}'.format(today.year, today.month, today.day)

        today_holiday = holidays_dict.get(today_str)
        if not today_holiday:
            raise HolidayNotFoundException()

        return today_holiday
