from myuw.views.page import page
from myuw.util.page_view import page_view


@page_view
def academic_calendar(request):
    context = {}
    return page(request, context, template='academic_calendar.html')
