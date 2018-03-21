from django.test import TestCase
from myuw.dao.registration import get_schedule_by_term
from uw_sws.models import Term
from restclients_core.exceptions import DataFailureException
from myuw.dao.textbook import get_textbook_by_schedule,\
    get_order_url_by_schedule
from myuw.test import get_request_with_user


class TestTextbooks(TestCase):

    def test_get_by_schedule(self):
        req = get_request_with_user('javerage')
        term = Term()
        term.year = 2013
        term.quarter = "summer"
        schedule = get_schedule_by_term(req, term)

        books = get_textbook_by_schedule(schedule)
        self.assertEquals(len(books), 1)
        self.assertEquals(books[13833][0].title,
                          "2 P/S Tutorials In Introductory Physics")

    def test_get_order_url_by_schedule(self):
        req = get_request_with_user('javerage')
        term = Term()
        term.year = 2013
        term.quarter = "spring"
        schedule = get_schedule_by_term(req, term)

        returned_link = get_order_url_by_schedule(schedule)

        expected_link = ('http://www.ubookstore.com/adoption-search-results?' +
                         'ccid=9335,1132,5320,2230,4405')
        self.assertEquals(returned_link, expected_link)

        term = Term()
        term.year = 2014
        term.quarter = "winter"
        schedule = get_schedule_by_term(req, term)
        self.assertRaises(DataFailureException,
                          get_order_url_by_schedule,
                          schedule)
