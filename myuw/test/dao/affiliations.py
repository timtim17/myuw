from django.test import TestCase
from django.conf import settings
from myuw.dao.affiliation import get_all_affiliations, get_identity_log_str
from myuw.test import fdao_sws_override, fdao_pws_override,\
    get_request, get_request_with_user


@fdao_pws_override
@fdao_sws_override
class TestAffilliations(TestCase):
    def setUp(self):
        get_request()

    def test_eos_enrollment(self):
        now_request = get_request_with_user('jeos')
        affiliations = get_all_affiliations(now_request)

    def test_fyp_enrollment(self):
        now_request = get_request_with_user('jnew')
        affiliations = get_all_affiliations(now_request)
        self.assertTrue(affiliations['fyp'])

    def test_is_faculty(self):
        now_request = get_request_with_user('bill')
        affiliations = get_all_affiliations(now_request)
        self.assertTrue(affiliations['faculty'])

    def test_is_clinician(self):
        now_request = get_request_with_user('eight')
        affiliations = get_all_affiliations(now_request)
        self.assertTrue(affiliations['clinician'])

    def test_is_pce_stud(self):
        now_request = get_request_with_user('jpce')
        affiliations = get_all_affiliations(now_request)
        self.assertTrue(affiliations['pce'])
        self.assertTrue('PCE-student' in get_identity_log_str(now_request))

        now_request = get_request_with_user('jeos')
        affiliations = get_all_affiliations(now_request)
        self.assertTrue(affiliations['pce'])
        self.assertTrue('PCE-student' in get_identity_log_str(now_request))
        self.assertTrue('Campuses: PCE' in get_identity_log_str(now_request))
