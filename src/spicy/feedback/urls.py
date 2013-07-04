from django.conf.urls.defaults import *

public_urls = patterns(
    'spicy.feedback.views',
    url(r'^new/$', 'new_feedback', name='new'),
)

admin_urls = patterns(
    'spicy.feedback.admin',
    url(r'^create/$', 'create', name='create'),
    url(r'^pattern/(?P<pattern_id>\d+)/$', 'edit_pattern', name='edit-pattern'),
    url(r'^pattern/attach/(?P<pattern_id>\d+)/$', 'pattern_media', name='edit-pattern-media'),

    url(r'^patterns/$', 'patterns', name='patterns'),
    url(r'^list/$', 'feedback_list', name='index'),

    url(r'^feedback/(?P<feedback_id>\d+)/$', 'detail', name='edit'),

    url(r'^delete_feedback/(?P<feedback_id>\d+)/$', 'delete', name='delete'),
    url(r'^delete_pattern/(?P<pattern_id>\d+)/$', 'delete_pattern', name='delete-pattern'),

    url(r'^list/delete/$', 'delete_list', name='message-delete'),
)

urlpatterns = patterns(
    '',
    url(r'^feedback/', include(public_urls, namespace='public')),
    url(r'^admin/feedback/', include(admin_urls, namespace='admin')),
)

