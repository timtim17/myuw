import re
from rc_django.cache_implementation import TimedCache
from rc_django.cache_implementation.memcache import MemcachedCache


FIVE_SECONDS = 5
FIFTEEN_MINS = 60 * 15
ONE_HOUR = 60 * 60
FOUR_HOURS = 60 * 60 * 4
ONE_DAY = 60 * 60 * 24
logger = logging.getLogger(__name__)


def get_cache_time(service, url):
    if "myplan" == service:
        return FIVE_SECONDS

    if "sws" == service:
        if re.match(r'^/student/v5/term/', url):
            return ONE_DAY

        if re.match(r'^/student/v5/person/', url):
            return ONE_HOUR

        if re.match(r'^/student/v5/course/', url):
            if re.match(r'^/student/v5/course/.*/status.json$', url):
                return ONE_HOUR
            return FIFTEEN_MINS * 2

        return FIFTEEN_MINS

    if "kws" == service:
        if re.match(r'^"/key/v1/encryption/', url):
            return ONE_DAY * 30
        return ONE_DAY * 7

    if "gws" == service:
        return FIFTEEN_MINS

    if "pws" == service:
        return ONE_HOUR

    if "uwnetid" == service:
        return ONE_HOUR

    return FOUR_HOURS


class MyUWMemcachedCache(MemcachedCache):

    def get_cache_expiration_time(self, service, url):
        return get_cache_time(service, url)


class MyUWCache(TimedCache):

    def getCache(self, service, url, headers):
        return self._response_from_cache(
            service, url, headers, get_cache_time(service, url))

    def processResponse(self, service, url, response):
        return self._process_response(service, url, response)
