# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from myuw.models import VisitedLinkNew, PopularLink
from myuw.dao import get_netid_of_current_user
from myuw.views.decorators import admin_required
from myuw.views import set_admin_wrapper_template

PAGE_SIZE = 10
MAX_PAGE = 5
logger = logging.getLogger(__name__)


@login_required
@admin_required
def popular_links(request, page):
    uwnetid = get_netid_of_current_user(request)
    if request.POST:
        if 'url' in request.POST and 'label' in request.POST:
            create_args = {'url': request.POST['url'],
                           'label': request.POST['label'],
                           }

            if request.POST['campus']:
                create_args['campus'] = request.POST['campus']

            if request.POST['affiliation']:
                create_args['affiliation'] = request.POST['affiliation']

            if 'pce' in request.POST and request.POST['pce'] == "pce":
                create_args['pce'] = True

            PopularLink.objects.create(**create_args)
            logger.info("popular link added.  user: {}, link: {}".format(
                uwnetid, request.POST['url']))

        if 'remove_popular' in request.POST:
            for popular_id in request.POST.getlist('remove_popular'):
                link = PopularLink.objects.get(pk=popular_id)
                url = link.url
                link.delete()
                logger.info("popular link removed. user: {}, link: {}".format(
                    uwnetid, url))

    curated_popular = PopularLink.objects.all()
    existing_lookup = set()
    curated_links = []
    for link in curated_popular:
        existing_lookup.add(link.url)
    kwargs = {}
    filter_kwargs = {}
    for field in ('campus', 'affiliation', 'pce'):
        if field in request.GET:
            value = request.GET[field]
            kwargs['is_'+value] = True
            if value != 'any_{}'.format(field):
                filter_kwargs['is_'+value] = True
                kwargs[field] = value
        else:
            kwargs['is_any_{}'.format(field)] = True

    # typo in the original model creation.  patching here to avoid a
    # db migration
    if 'is_undergrad' in filter_kwargs:
        del filter_kwargs['is_undergrad']
        filter_kwargs['is_undegrad'] = True

    all_popular = VisitedLinkNew.get_popular(**filter_kwargs)

    # Display is 1-indexed, we're 0-indexed
    page = int(page)
    page -= 1
    if page > MAX_PAGE or page < 0:
        page = 0

    start_index = page * PAGE_SIZE
    popular = all_popular[start_index:start_index+PAGE_SIZE]

    for link in popular:
        if link['url'] in existing_lookup:
            link['exists'] = True
        else:
            link['exists'] = False

    context = {'popular': popular,
               'checked': kwargs,
               'curated_popular_links': curated_popular,
               }

    if page > 0:
        context['previous_page'] = reverse('myuw_popular_links_paged',
                                           kwargs={'page': page})

    if page+1 < MAX_PAGE and len(all_popular) > start_index+PAGE_SIZE:
        context['next_page'] = reverse('myuw_popular_links_paged',
                                       kwargs={'page': page+2})
    set_admin_wrapper_template(context)
    return render(request, "admin/popular_links.html", context)
