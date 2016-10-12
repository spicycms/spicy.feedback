from django import http
from django.db.models import Q
from django.shortcuts import get_object_or_404
from spicy.core.siteskin.decorators import ajax_request
from spicy.core.siteskin.decorators import multi_view
from spicy.utils import load_module, get_custom_model_class
from rest_framework.authtoken.models import Token
from django.core.paginator import Paginator
from . import defaults, models, signals
import requests
import json

Feedback = get_custom_model_class(defaults.CUSTOM_FEEDBACK_MODEL)


@ajax_request
def new_feedback(request):
    """
    Render form for adding feedback to consumer with type and id.
    After adding feedback redirects to consumer absolute url
    """
    FeedbackForm = load_module(defaults.CUSTOM_FEEDBACK_FORM)

    if request.method == 'GET':
        from django.shortcuts import render
        return render(request, 'spicy.core.simplepages/simplepages/feedback_create_lead.html')

    if request.method == 'POST':
        pattern = get_object_or_404(
            models.FeedbackPattern, slug=request.POST.get('pattern'))
        feedback = Feedback(pattern=pattern)
        form = FeedbackForm(request.POST, instance=feedback)

        if form.is_valid():
            if 'import requests' in request.session:
                del request.session['feedback_form']
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

            signals.create_feedback.send(
                sender=feedback.__class__, request=request, feedback=feedback)

            if pattern.token:
                url_to_api = pattern.url_to_api
                token = Token.objects.get(user__email=feedback.email)
                if token and url_to_api:
                    full_request = request.POST.copy()
                    full_request.update({'lead_source': request.META.get('HTTP_HOST')})
                    headers = {'Authorization': 'Token %s' % token.key, 'content-type': 'application/json'}
                    data = json.dumps(full_request)
                    requests.post(url_to_api, data=data, headers=headers)

            if feedback.processing_status != defaults.SPAM:
                feedback.send_report()

            try:
                if defaults.SEND_AUTO_RESPONSE_WITHOUT_TIMEOUT:
                    feedback.send_to_customers(realhost=request.get_host())
            except Exception as e:
                return {'status': 'success', 'errors': e.message}

            return {'status': 'success'}
        else:
            request.session['feedback_form'] = request.POST
            return {'status': 'fail', 'errors': str(form.errors)}
    else:
        return http.HttpResponseNotAllowed(['POST'])


@multi_view()
def any_feedback(request, template):
    try:
        page_num = int(request.GET.get('page', 1))
    except ValueError:
        page_num = 1
    search_args = []
    search_text = request.GET.get('search_text')
    if search_text:
        search_args.append(
            Q(var1__icontains=search_text) |
            Q(message__icontains=search_text))
    filter_name = request.GET.get('filter_name')
    filter_value = request.GET.get('filter_value')
    if filter_name and filter_value:
        search_args.append(Q(**{'%s__icontains' % filter_name: filter_value}))
    search_args.append(Q(processing_status=defaults.PUBLISHED))
    items = Feedback.objects.filter(*search_args)
    paginator = Paginator(items, defaults.FEEDBACK_PER_PAGE)
    page = paginator.page(page_num)
    paginator.current_page = page
    objects_list = page.object_list
    if template.replace('/','').split(".")[-1] != 'html':
        template = template.replace('/','') + '.html'
    return dict(items=objects_list, paginator=paginator, template=template)
