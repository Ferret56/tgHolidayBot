from app.utils.country_mapper import mapper
import datetime
from app.requests.holiday import HolidayRequests
from app.parsers.holiday import HolidayParser
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s :: %(levelname)s :: %(message)s')


class CountryNotFoundException(Exception):
    def __init__(self, message):
        self.message = message


class HolidayNotFoundException(Exception):
    def __init__(self, message=None):
        self.message = message


class HolidayServiceException(Exception):
    def __init__(self, message=None):
        self.message = message


class HolidayService:
    @staticmethod
    def get_current_holiday_in_country(country_cyrillic: str) -> dict:
        country_latin = mapper.get(country_cyrillic.lower())
        if not country_latin:
            raise CountryNotFoundException('Страна {} не найдена в каталоге'
                                           .format(country_cyrillic))

        try:
            get_holiday_page_html = HolidayRequests.holidays_request_by_country(country_latin)
        except Exception as ex:
            logging.error('Ошибка при обработке запроса. ' + str(ex))
            raise HolidayServiceException(str(ex))
        try:
            holidays_dict = HolidayParser.parse_holidays_country_page(get_holiday_page_html)
        except Exception as ex:
            logging.error('Ошибка при парсинге запроса. ' + str(ex))
            raise HolidayServiceException(str(ex))

        today = datetime.date.today()
        today_str = '{}-{}-{}'.format(today.year, today.month, today.day)

        today_holiday = holidays_dict.get(today_str)
        if not today_holiday:
            raise HolidayNotFoundException()

        return today_holiday
