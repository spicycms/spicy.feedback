from django.conf.urls.defaults import *

public_urls = patterns(
    'spicy.feedback.views',
    url(r'^new/$', 'new_feedback', name='new-feedback'),

)

admin_urls = patterns(
    'spicy.feedback.admin',
    url(r'^messages/$', 'messages', name='index'),
    url(r'^messages/(?P<message_id>\d+)/$', 'message_details', name='message-details'),
    url(r'^messages/delete/$', 'messages_delete', name='message-delete'),

)

urlpatterns = patterns(
    '',
    url(r'^feedback/', include(public_urls, namespace='public')),
    url(r'^feedback/admin/', include(admin_urls, namespace='admin')),
)

