from django import http
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import get_object_or_404
from spicy.core.siteskin.decorators import ajax_request
from spicy.core.siteskin.decorators import render_to, multi_view
from spicy.utils import load_module, get_custom_model_class, NavigationFilter
from django.core.paginator import Paginator
from . import defaults, models


Feedback = get_custom_model_class(defaults.CUSTOM_FEEDBACK_MODEL)


@ajax_request
def new_feedback(request):
    """
    Render form for adding feedback to consumer with type and id.
    After adding feedback redirects to consumer absolute url
    """
    FeedbackForm = load_module(defaults.CUSTOM_FEEDBACK_FORM)

    if request.method == 'POST':
        pattern = get_object_or_404(
            models.FeedbackPattern, slug=request.POST.get('pattern'))
        feedback = Feedback(pattern=pattern)
        form = FeedbackForm(request.POST, instance=feedback)

        if form.is_valid():
            try:
                del request.session['feedback_form']
            except KeyError:
                pass
            feedback = form.save(commit=False)
            feedback.ip_address = request.META['REMOTE_ADDR']
            if not (
                    feedback.name.strip() or feedback.email.strip() or
                    feedback.phone.strip() or feedback.var1.strip() or
                    feedback.var2.strip() or feedback.var3.strip() or
                    feedback.message.strip() or
                    feedback.company_name.strip() or feedback.url.strip()):
                feedback.processing_status = defaults.SPAM
            feedback.save()

            try:
                from spicy.marketing.models import Visitor
                from spicy.crm.models import Lead
                if getattr(request.session, 'session_key', None):
                    visitors = Visitor.objects.filter(
                        session_key=request.session.session_key,
                        lead__isnull=True)
                    if visitors:
                        visitor = visitors[0]
                        visitor.lead = Lead.objects.get(
                            consumer_type=ContentType.objects.get_for_model(
                                feedback),
                            consumer_id=feedback.pk)
                        visitor.save()
            except ImportError:
                pass

            if feedback.processing_status != defaults.SPAM:
                feedback.send_report()

            if defaults.SEND_AUTO_RESPONSE_WITHOUT_TIMEOUT:
                feedback.send_to_customers()

            return {'status': 'success'}
        else:
            request.session['feedback_form'] = request.POST
            return {'status': 'error', 'errors': str(form.errors)}
    else:
        return http.HttpResponseNotAllowed(['POST'])


@multi_view()
def any_feedback(request, template):
    try:
        page_num = int(request.GET.get('page', 1))
    except ValueError:
        page_num = 1
    search_args, search_kwargs = [], {}
    search_text = request.GET.get('search_text')
    if search_text:
        search_args.append(
            Q(var1__icontains=search_text) |
            Q(message__icontains=search_text))
    filter_name = request.GET.get('filter_name')
    filter_value = request.GET.get('filter_value')
    if filter_name and filter_value:
        search_args.append(Q(**{'%s__icontains' % filter_name: filter_value}))
    search_args.append(Q(processing_status=defaults.PUBLISHED))#PUBLISHED
    items = Feedback.objects.filter(*search_args)
    paginator = Paginator(items, defaults.FEEDBACK_PER_PAGE)
    page = paginator.page(page_num)
    paginator.current_page = page
    objects_list = page.object_list
    return dict(items=objects_list, paginator=paginator, template=template)
