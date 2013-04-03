from . import models
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from spicy.core.profile.decorators import is_staff
from spicy.core.siteskin.decorators import render_to, ajax_request
from spicy.utils import NavigationFilter


@is_staff(required_perms='feedback.change_message')
@render_to('feedback/admin/messages.html')
def messages(request):
    nav = NavigationFilter(request)
    paginator = nav.get_queryset_with_paginator(models.Message)
    objects_list = paginator.current_page.object_list
    return {'paginator': paginator, 'objects_list': objects_list, 'nav': nav}


@is_staff(required_perms='feedback.change_message')
@render_to('feedback/admin/message_details.html')
def message_details(request, message_id):
    message = get_object_or_404(models.Message, pk=message_id)
    context = {'message_obj': message}
    context.update(message.get_goals_data())
    return context


@is_staff(required_perms='feedback.delete_message')
@ajax_request
def messages_delete(request):
    message = ''
    status = 'ok'
    try:
        for message in models.Message.objects.filter(
            id__in=request.POST.getlist('id')):
            message.delete()
        message = _('All objects have been deleted successfully')
    except KeyError:
        message = settings.MESSAGES['error']
        status = 'error'
    except Exception, e:
        print e
    return dict(message=unicode(message), status=status)
