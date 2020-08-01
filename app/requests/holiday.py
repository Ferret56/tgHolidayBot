import requests
from app.config import calendar_holidays_url
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s :: %(levelname)s :: %(message)s')


class HolidayRequestException(Exception):
    def __init__(self, message):
        super.__init__(message)


class HolidayRequests:
    @staticmethod
    def holidays_request_by_country(country_name: str):
        r = requests.get(url=calendar_holidays_url + '/' + country_name)
        # so bad
        if not r:
            logging.error({'holidays_by_country_request': {
                'request_url': r.request.url,
                'response_status': r.status_code,
                'response_text': r.text
            }})
            raise HolidayRequestException('Ошибка при отправке запроса на {}'
                                          .format(r.request.url))
        # so good
        logging.info({'holidays_by_country_request': {
            'request_url': r.request.url,
            'response_status': r.status_code
        }})

        return r.text
