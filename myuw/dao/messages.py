import csv
import os
import datetime
import bleach
from dateutil.parser import parse
from myuw.models import BannerMessage
from myuw.dao import is_netid_in_list, get_netid_of_current_user
from myuw.dao.term import get_comparison_datetime
from myuw.dao.affiliation import get_all_affiliations
from myuw.dao.affiliation_data import get_data_for_affiliations
from authz_group import Group
from django.utils import timezone

MESSAGE_ALLOWED_TAGS = bleach.sanitizer.ALLOWED_TAGS + ["span", "h1", "h2",
                                                        "h3", "h4"]
MESSAGE_ALLOWED_ATTRIBUTES = bleach.sanitizer.ALLOWED_ATTRIBUTES.copy()
MESSAGE_ALLOWED_ATTRIBUTES["*"] = ["class", "style", "aria-hidden"]
MESSAGE_ALLOWED_STYLES = ["font-size", "color"]


def get_current_messages(request):
    current_date = get_comparison_datetime(request)
    affiliations = get_all_affiliations(request)

    current_date = timezone.make_aware(current_date)

    messages = get_data_for_affiliations(model=BannerMessage,
                                         affiliations=affiliations,
                                         start__lte=current_date,
                                         end__gte=current_date,
                                         is_published=True)

    filtered = []
    user = get_netid_of_current_user(request)
    g = Group()
    for message in messages:
        if message.group_id:
            if not g.is_member_of_group(user, message.group_id):
                continue
        filtered.append(message)

    preview_id = request.GET.get('banner', None)
    if preview_id:
        try:
            banner = BannerMessage.objects.get(preview_id=preview_id)
            filtered.append(banner)
        except BannerMessage.DoesNotExist:
            pass
    return filtered


def clean_html(input, additional_tags=None):
    tags = MESSAGE_ALLOWED_TAGS
    if additional_tags:
        tags += additional_tags

    return bleach.clean(input, tags=tags,
                        attributes=MESSAGE_ALLOWED_ATTRIBUTES,
                        styles=MESSAGE_ALLOWED_STYLES)
