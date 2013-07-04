from django.conf import settings
from django import http
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from spicy.core.admin.conf import AdminAppBase, AdminLink, Perms
from spicy.core.profile.decorators import is_staff
from spicy.core.siteskin.decorators import render_to, ajax_request
from spicy.utils import NavigationFilter
from spicy.utils.models import get_custom_model_class

from . import models, defaults, forms

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

    perms = Perms(view=[],  write=[], manage=[])

    @render_to('menu.html', use_admin=True)
    def menu(self, request, *args, **kwargs):
        return dict(app=self, *args, **kwargs)

    @render_to('dashboard.html', use_admin=True)
    def dashboard(self, request, *args, **kwargs):
        return dict(app=self, *args, **kwargs)


@is_staff(required_perms='feedback.admin_feedback')
@render_to('create.html', use_admin=True)
def create(request):
    message = ''

    pattern = None
    
    if request.method == 'POST':
        form = forms.CreatePatternForm(request.POST)
        if form.is_valid():
            pattern = form.save()
        else:
            message = 'Form validation Error: ' + str(form.errors)

        if pattern is not None:
            return http.HttpResponseRedirect(
                reverse('feedback:admin:edit-pattern', args=[pattern.pk]))
    else:
        form = forms.CreatePatternForm()

    return dict(form=form, message=message)


@is_staff(required_perms='feedback.admin_feedback')
@render_to('edit_pattern.html', use_admin=True)
def edit_pattern(request, pattern_id):
    message = ''

    pattern = get_object_or_404(models.FeedbackPattern, pk=pattern_id)
    
    if request.method == 'POST':
        form = forms.PatternForm(request.POST, instance=pattern)
        # fromset

        if form.is_valid():
            pattern = form.save()
        else:
            message = 'Form validation Error: ' + str(form.errors)
    else:
        form = forms.PatternForm(instance=pattern)

    return dict(form=form, message=message)

@is_staff(required_perms='feedback.admin_feedback')
@render_to('edit_pattern_media.html', use_admin=True)
def pattern_media(request, pattern_id):
    status = ''
    message = ''
    
    pattern = get_object_or_404(models.FeedbackPattern, pk=pattern_id)
    form = forms.PatternForm(instance=pattern)

    return dict(status=status, message=message, form=form)


@is_staff(required_perms='feedback.admin_feedback')
@render_to('list.html', use_admin=True)
def feedback_list(request):
    nav = NavigationFilter(request)
    paginator = nav.get_queryset_with_paginator(Feedback)
    objects_list = paginator.current_page.object_list        
    return {'paginator': paginator, 'objects_list': objects_list, 'nav': nav}


@is_staff(required_perms='feedback.admin_feedback')
@render_to('patterns.html', use_admin=True)
def patterns(request):
    nav = NavigationFilter(request)
    paginator = nav.get_queryset_with_paginator(models.FeedbackPattern)
    objects_list = paginator.current_page.object_list        
    return {'paginator': paginator, 'objects_list': objects_list, 'nav': nav}


@is_staff(required_perms='feedback.admin_feedback')
@render_to('edit.html', use_admin=True)
def detail(request, feedback_id):
    feedback = get_object_or_404(Feedback, pk=feedback_id)
    if request.method == 'POST':
        form = forms.EditFeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            feedback = form.save()
        else:
            message = 'Form validation Error: ' + str(form.errors)
    else:
        form = forms.EditFeedbackForm(instance=feedback)

    return dict(form=form)


@is_staff(required_perms='feedback.admin_feedback')
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


@is_staff(required_perms='feedback.admin_feedback')
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


@is_staff(required_perms='feedback.admin_feedback')
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
