from django.test import TestCase
from restclients.mock_http import MockHTTP
from myuw.util.cache_implementation import MyUWCache
from restclients.models import CacheEntryTimed
from datetime import timedelta


CACHE = 'myuw.util.cache_implementation.MyUWCache'


class TestCustomCachePolicy(TestCase):
    def test_sws_default_policies(self):
        with self.settings(RESTCLIENTS_DAO_CACHE_CLASS=CACHE):
            cache = MyUWCache()
            ok_response = MockHTTP()
            ok_response.status = 200
            ok_response.data = "xx"

            response = cache.getCache('sws', '/student/myuwcachetest1', {})
            self.assertEquals(response, None)
            cache.processResponse("sws",
                                  "/student/myuwcachetest1",
                                  ok_response)
            response = cache.getCache('sws', '/student/myuwcachetest1', {})
            self.assertEquals(response["response"].data, 'xx')

            cache_entry = CacheEntryTimed.objects.get(
                service="sws",
                url="/student/myuwcachetest1")
            # Cached response is returned after 3 hours and 58 minutes
            orig_time_saved = cache_entry.time_saved
            cache_entry.time_saved = (orig_time_saved -
                                      timedelta(minutes=(60 * 4)-2))
            cache_entry.save()

            response = cache.getCache('sws', '/student/myuwcachetest1', {})
            self.assertNotEquals(response, None)

            # Cached response is not returned after 4 hours and 1 minute
            cache_entry.time_saved = (orig_time_saved -
                                      timedelta(minutes=(60 * 4)+1))
            cache_entry.save()

            response = cache.getCache('sws', '/student/myuwcachetest1', {})
            self.assertEquals(response, None)

    def test_sws_term_policy(self):
        with self.settings(RESTCLIENTS_DAO_CACHE_CLASS=CACHE):
            cache = MyUWCache()
            ok_response = MockHTTP()
            ok_response.status = 200
            ok_response.data = "xx"

            response = cache.getCache(
                'sws', '/student/v5/term/1014,summer.json', {})
            self.assertEquals(response, None)
            cache.processResponse(
                "sws", "/student/v5/term/1014,summer.json", ok_response)
            response = cache.getCache(
                'sws', '/student/v5/term/1014,summer.json', {})
            self.assertEquals(response["response"].data, 'xx')

            cache_entry = CacheEntryTimed.objects.get(
                service="sws", url="/student/v5/term/1014,summer.json")
            # Cached response is returned after 6 days
            orig_time_saved = cache_entry.time_saved
            cache_entry.time_saved = orig_time_saved - timedelta(
                minutes=(60*24*7-1))
            cache_entry.save()

            response = cache.getCache(
                'sws', '/student/v5/term/1014,summer.json', {})
            self.assertNotEquals(response, None)

            # Cached response is not returned after 7 days
            cache_entry.time_saved = orig_time_saved - timedelta(days=7)
            cache_entry.save()

            response = cache.getCache(
                'sws', '/student/v5/term/current.json', {})
            self.assertEquals(response, None)

            response = cache.getCache(
                'sws', '/student/v5/term/current.json', {})
            self.assertEquals(response, None)
            cache.processResponse(
                "sws", "/student/v5/term/current.json", ok_response)
            response = cache.getCache(
                'sws', '/student/v5/term/current.json', {})
            self.assertEquals(response["response"].data, 'xx')

            cache_entry = CacheEntryTimed.objects.get(
                service="sws", url="/student/v5/term/current.json")
            # Cached response is returned after 6 days
            orig_time_saved = cache_entry.time_saved
            cache_entry.time_saved = orig_time_saved - timedelta(
                minutes=(60*24-1))
            cache_entry.save()

            response = cache.getCache(
                'sws', '/student/v5/term/current.json', {})
            self.assertNotEquals(response, None)

            # Cached response is not returned after 7 days
            cache_entry.time_saved = orig_time_saved - timedelta(days=1)
            cache_entry.save()

            response = cache.getCache(
                'sws', '/student/v5/term/current.json', {})
            self.assertEquals(response, None)

    def test_myplan_default(self):
        with self.settings(RESTCLIENTS_DAO_CACHE_CLASS=CACHE):
            cache = MyUWCache()
            ok_response = MockHTTP()
            ok_response.status = 200
            ok_response.data = "xx"

            response = cache.getCache('myplan', '/api/plan/xx', {})
            self.assertEquals(response, None)
            cache.processResponse("myplan", "/api/plan/xx", ok_response)
            response = cache.getCache('myplan', '/api/plan/xx', {})

            cache_entry = CacheEntryTimed.objects.get(
                service="myplan", url="/api/plan/xx")
            orig_time_saved = cache_entry.time_saved
            cache_entry.time_saved = (orig_time_saved -
                                      timedelta(seconds=5))
            cache_entry.save()
            response = cache.getCache('myplan', '/api/plan/xx', {})
            self.assertEquals(response, None)

    def test_registration_default(self):
        with self.settings(RESTCLIENTS_DAO_CACHE_CLASS=CACHE):
            cache = MyUWCache()
            ok_response = MockHTTP()
            ok_response.status = 200
            ok_response.data = "xx"

            response = cache.getCache('sws', '/student/v5/registration/xx', {})
            self.assertEquals(response, None)
            cache.processResponse(
                "sws", "/student/v5/registration/xx", ok_response)
            response = cache.getCache(
                'sws', '/student/v5/registration/xx', {})

            cache_entry = CacheEntryTimed.objects.get(
                service="sws", url="/student/v5/registration/xx")
            orig_time_saved = cache_entry.time_saved
            cache_entry.time_saved = (orig_time_saved -
                                      timedelta(minutes=15))
            cache_entry.save()
            response = cache.getCache('sws', '/student/v5/registration/xx', {})
            self.assertEquals(response, None)

    def test_course_default(self):
        with self.settings(RESTCLIENTS_DAO_CACHE_CLASS=CACHE):
            cache = MyUWCache()
            ok_response = MockHTTP()
            ok_response.status = 200
            ok_response.data = "xx"

            response = cache.getCache('sws', '/student/v5/course/xx', {})
            self.assertEquals(response, None)
            cache.processResponse(
                "sws", "/student/v5/course/xx", ok_response)
            response = cache.getCache(
                'sws', '/student/v5/course/xx', {})

            cache_entry = CacheEntryTimed.objects.get(
                service="sws", url="/student/v5/course/xx")
            orig_time_saved = cache_entry.time_saved
            cache_entry.time_saved = (orig_time_saved -
                                      timedelta(minutes=60))
            cache_entry.save()
            response = cache.getCache('sws', '/student/v5/course/xx', {})
            self.assertEquals(response, None)

    def test_enrollment_default(self):
        with self.settings(RESTCLIENTS_DAO_CACHE_CLASS=CACHE):
            cache = MyUWCache()
            ok_response = MockHTTP()
            ok_response.status = 200
            ok_response.data = "xx"

            response = cache.getCache('sws', '/student/v5/enrollment/xx', {})
            self.assertEquals(response, None)
            cache.processResponse(
                "sws", "/student/v5/enrollment/xx", ok_response)
            response = cache.getCache(
                'sws', '/student/v5/enrollment/xx', {})

            cache_entry = CacheEntryTimed.objects.get(
                service="sws", url="/student/v5/enrollment/xx")
            orig_time_saved = cache_entry.time_saved
            cache_entry.time_saved = (orig_time_saved -
                                      timedelta(minutes=60))
            cache_entry.save()
            response = cache.getCache('sws', '/student/v5/enrollment/xx', {})
            self.assertEquals(response, None)

    def test_notice_default(self):
        with self.settings(RESTCLIENTS_DAO_CACHE_CLASS=CACHE):
            cache = MyUWCache()
            ok_response = MockHTTP()
            ok_response.status = 200
            ok_response.data = "xx"

            response = cache.getCache('sws', '/student/v5/notice/xx', {})
            self.assertEquals(response, None)
            cache.processResponse(
                "sws", "/student/v5/notice/xx", ok_response)
            response = cache.getCache(
                'sws', '/student/v5/notice/xx', {})

            cache_entry = CacheEntryTimed.objects.get(
                service="sws", url="/student/v5/notice/xx")
            orig_time_saved = cache_entry.time_saved
            cache_entry.time_saved = (orig_time_saved -
                                      timedelta(minutes=60))
            cache_entry.save()
            response = cache.getCache('sws', '/student/v5/notice/xx', {})
            self.assertEquals(response, None)

    def test_default_policies(self):
        with self.settings(RESTCLIENTS_DAO_CACHE_CLASS=CACHE):
            cache = MyUWCache()
            ok_response = MockHTTP()
            ok_response.status = 200
            ok_response.data = "xx"

            response = cache.getCache('no_such', '/student/myuwcachetest1', {})
            self.assertEquals(response, None)
            cache.processResponse(
                "no_such", "/student/myuwcachetest1", ok_response)
            response = cache.getCache('no_such', '/student/myuwcachetest1', {})
            self.assertEquals(response["response"].data, 'xx')

            cache_entry = CacheEntryTimed.objects.get(
                service="no_such", url="/student/myuwcachetest1")
            # Cached response is returned after 3 hours and 58 minutes
            orig_time_saved = cache_entry.time_saved
            cache_entry.time_saved = (orig_time_saved -
                                      timedelta(minutes=(60 * 4)-2))
            cache_entry.save()

            response = cache.getCache('no_such', '/student/myuwcachetest1', {})
            self.assertNotEquals(response, None)

            # Cached response is not returned after 4 hours and 1 minute
            cache_entry.time_saved = (orig_time_saved -
                                      timedelta(minutes=(60 * 4)+1))
            cache_entry.save()

            response = cache.getCache('no_such', '/student/myuwcachetest1', {})
            self.assertEquals(response, None)
