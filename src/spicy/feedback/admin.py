from django import http
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import transaction
from django.forms import ModelForm
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from spicy.core.admin.conf import AdminAppBase, AdminLink, Perms
from spicy.core.profile.decorators import is_staff
from spicy.core.siteskin.decorators import render_to, ajax_request
from spicy.utils import NavigationFilter, load_module, get_custom_model_class
from . import abs, models, defaults, forms

Feedback = get_custom_model_class(defaults.CUSTOM_FEEDBACK_MODEL)


class AdminApp(AdminAppBase):
    name = 'feedback'
    label = _('Feedbacks')
    order_number = 4

    menu_items = (
        AdminLink('feedback:admin:create', _('Create pattern')),
        AdminLink('feedback:admin:patterns', _('All patterns')),
        AdminLink('feedback:admin:index', _('All feedbacks')),
    )

    create = AdminLink('feedback:admin:create', _('Create pattern'),)

    perms = Perms(view=[],  write=[], manage=[])

    @render_to('menu.html', use_admin=True)
    def menu(self, request, *args, **kwargs):
        return dict(app=self, *args, **kwargs)

    @render_to('dashboard.html', use_admin=True)
    def dashboard(self, request, *args, **kwargs):
        return dict(app=self, *args, **kwargs)


@is_staff(required_perms='feedback.add_feedbackpattern')
@render_to('create.html', use_admin=True)
def create(request):
    message = ''

    pattern = None

    if request.method == 'POST':
        form = forms.PatternForm(request.POST)
        if form.is_valid():
            pattern = form.save()
        else:
            message = 'Form validation Error: ' + str(form.errors)

        if pattern is not None:
            return http.HttpResponseRedirect(
                reverse('feedback:admin:edit-pattern', args=[pattern.pk]))
    else:
        form = forms.PatternForm()

    return dict(form=form, message=message)


def _backend_data(pattern, backend_name=None):
    backend_modules = [
        load_module(backend) for backend in defaults.FEEDBACK_BACKENDS]
    backends = [
        (backend.admin_form[0], backend.__name__.rsplit('.', 1)[-1])
        for backend in backend_modules if backend.admin_form]
    help_text = None
    if backend_name:
        for backend in backend_modules:
            if backend.__name__.rsplit('.', 1)[-1] == backend_name:
                tab = backend_name
                title = backend.admin_form[0]

                class Meta:
                    model = models.FeedbackPattern
                    fields = backend.admin_form[1]
                Form = type(
                    'CustomFeedback', (ModelForm,), {'Meta': Meta})
                help_text = getattr(backend, 'admin_help', None)
    else:
        Form = forms.PatternForm
        tab = 'edit'
        title = _('Edit pattern: %s') % pattern
    return locals()


@is_staff(required_perms='feedback.change_feedbackpattern')
@render_to('edit_pattern.html', use_admin=True)
def edit_pattern(request, pattern_id, backend_name=None):
    message = ''

    pattern = get_object_or_404(models.FeedbackPattern, pk=pattern_id)
    data = _backend_data(pattern, backend_name)
    Form = data.pop('Form')

    if request.method == 'POST':
        form = Form(request.POST, instance=pattern)
        if form.is_valid():
            pattern = form.save()
            message = _('Object has been saved successfully')
        else:
            message = _('Form validation Error: ') + unicode(form.errors)
    else:
        form = Form(instance=pattern)

    return dict(form=form, message=message, **data)


@is_staff(required_perms='feedback.change_feedbackpattern')
@render_to('edit_pattern_media.html', use_admin=True)
def pattern_media(request, pattern_id):
    status = ''
    message = ''

    pattern = get_object_or_404(models.FeedbackPattern, pk=pattern_id)
    data = _backend_data(pattern)
    data.pop('tab')
    form = forms.PatternForm(instance=pattern)

    return dict(
        status=status, message=message, form=form, tab='media', **data)


@is_staff(required_perms='feedback.change_feedback')
@render_to('list.html', use_admin=True)
def feedback_list(request):
    nav = NavigationFilter(request)
    paginator = nav.get_queryset_with_paginator(Feedback)
    objects_list = paginator.current_page.object_list
    return {'paginator': paginator, 'objects_list': objects_list, 'nav': nav}


@is_staff(required_perms='feedback.change_feedback')
@render_to('patterns.html', use_admin=True)
def patterns(request):
    nav = NavigationFilter(request)
    paginator = nav.get_queryset_with_paginator(models.FeedbackPattern)
    objects_list = paginator.current_page.object_list
    return {'paginator': paginator, 'objects_list': objects_list, 'nav': nav}


@is_staff(required_perms='feedback.change_feedback')
@render_to('edit.html', use_admin=True)
def detail(request, feedback_id):
    feedback = get_object_or_404(Feedback, pk=feedback_id)
    message = ''
    status = 'ok'
    if request.method == 'POST':
        form = forms.EditFeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            feedback = form.save()
        else:
            status = 'error'
            message = _('Form validation Error: ') + unicode(form.errors)
    else:
        form = forms.EditFeedbackForm(instance=feedback)

    return dict(form=form, message=message, status=status)


@is_staff(required_perms='feedback.delete_feedback')
@render_to('delete.html', use_admin=True)
def delete(request, feedback_id):
    message = ''
    status = 'ok'

    instance = get_object_or_404(Feedback, pk=feedback_id)
    if request.method == 'POST':
        if 'confirm' in request.POST:
            instance.delete()
            return http.HttpResponseRedirect(
                reverse('feedback:admin:index'))

    return dict(message=unicode(message), status=status, instance=instance)


@is_staff(required_perms='feedback.delete_feedbackpattern')
@render_to('delete.html', use_admin=True)
def delete_pattern(request, pattern_id):
    message = ''
    status = 'ok'

    instance = get_object_or_404(models.FeedbackPattern, pk=pattern_id)
    if request.method == 'POST':
        if 'confirm' in request.POST:
            instance.delete()
            return http.HttpResponseRedirect(
                reverse('feedback:admin:patterns'))

    return dict(message=unicode(message), status=status, instance=instance)


@is_staff(required_perms='feedback.delete_feedback')
@ajax_request
def delete_list(request):
    message = ''
    status = 'ok'
    try:
        for message in Feedback.objects.filter(
                id__in=request.POST.getlist('id')):
            message.delete()
        message = _('All objects have been deleted successfully')
    except KeyError:
        message = settings.MESSAGES['error']
        status = 'error'
    except Exception, e:
        print e
    return dict(message=unicode(message), status=status)


@is_staff()
@render_to('provider_form.html', use_admin=True)
def provider_form(request, consumer_type, consumer_id, field_name):
    default_pattern = models.FeedbackPattern.objects.all()[:1]
    initial = {'pattern': default_pattern[0]} if default_pattern else None
    form = forms.ProviderForm(initial=initial)
    fields = (
        'name', 'email', 'phone', 'message', 'company_name', 'url', 'var1',
        'var2', 'var3')
    fields_data = []
    for field in fields:
        field_data = {
            'name': field,
            'label': unicode(
                abs.BaseFeedbackAbstractModel._meta.get_field_by_name(
                    field)[0].verbose_name)}
        fields_data.append(field_data)
    return {
        'form': form, 'consumer_type': consumer_type, 'fields': fields_data,
        'consumer_id': consumer_id, 'field_name': field_name,
        'field_types': defaults.FEEDBACK_VAR_CHOICES}


@is_staff()
@ajax_request
@transaction.commit_on_success
def create_provider(request, consumer_type, consumer_id):
    content_type = get_object_or_404(ContentType, model=consumer_type)
    model = content_type.model_class()
    get_object_or_404(model, pk=consumer_id)
    sid = transaction.savepoint()
    status = 'error'
    message = ''
    prov_id = None
    prov = models.FeedbackPatternProvider(
        consumer_type=content_type, consumer_id=consumer_id)
    provider_form = forms.ProviderForm(
        request.POST, instance=prov)
    try:
        prov = models.FeedbackPatternProvider(
            consumer_type=content_type, consumer_id=consumer_id)
        provider_form = forms.ProviderForm(
            request.POST, instance=prov)
        if provider_form.is_valid():
            prov = provider_form.save()
            prov_id = prov.id
        else:
            raise Exception('Form error')
        fields_cnt = provider_form.cleaned_data['fields_cnt']
        pos = 0
        for i in xrange(fields_cnt):
            var = models.FeedbackPatternProviderVariable(
                provider=prov, position=pos)
            var_form = forms.FeedbackVariableForm(
                request.POST, prefix='fields_%i' % i, instance=var)
            if var_form.is_valid():
                pos += 1
                var = var_form.save()
                if var.field_type in defaults.FEEDBACK_VARS_WITH_OPTIONS:
                    options_cnt = var_form.cleaned_data['options_cnt']
                    sub_pos = 0
                    for j in xrange(options_cnt):
                        option = models.FeedbackVariableOption(
                            variable=var, position=sub_pos)
                        option_form = forms.FeedbackOptionForm(
                            request.POST, instance=option,
                            prefix='fields_{}_{}'.format(i, j))
                        if option_form.is_valid():
                            sub_pos += 1
                            option = option_form.save()

        transaction.savepoint_commit(sid)
        status = 'ok'
    except Exception:
        transaction.savepoint_rollback(sid)
        message = _('Error processing form data')
    return {
        'status': status, 'message': unicode(message),
        'provider_id': prov_id if status == 'ok' else None}
