from django import http
from django.shortcuts import get_object_or_404
from spicy.core.siteskin.decorators import ajax_request
from spicy.utils import load_module, get_custom_model_class
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
