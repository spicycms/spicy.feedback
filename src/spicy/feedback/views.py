from django import http
from spicy.core.siteskin.decorators import ajax_request
from . import forms

@ajax_request
def new_feedback(request):
    """
    Render form for adding feedback to consumer with type and id.
    After adding feedback redirects to consumer absolute url
    """
    if request.method == 'POST':
        form = forms.MessageForm(request.POST)

        if form.is_valid():
            try:
                del request.session['feedback_form']
            except KeyError:
                pass
            feedback = form.save(commit=False)
            feedback.ip_address = request.META['REMOTE_ADDR']
            feedback.save()
            feedback.send_report()
            return {'status': 'success'}
        else:
            request.session['feedback_form'] = request.POST
            return {'status': 'error', 'errors': str(form.errors)}
    else:
        return http.HttpResponseNotAllowed(['POST'])
