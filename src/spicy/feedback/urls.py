from django.conf.urls.defaults import patterns, url, include

public_urls = patterns(
    'spicy.feedback.views',
    url(r'^new/$', 'new_feedback', name='new'),
)

admin_urls = patterns(
    'spicy.feedback.admin',
    url(r'^create/$', 'create', name='create'),
    url(
        r'^patterns/(?P<pattern_id>\d+)/$', 'edit_pattern',
        name='edit-pattern'),
    url(
        r'^patterns/(?P<pattern_id>\d+)/extra/(?P<backend_name>\w+)/$',
        'edit_pattern', name='edit-pattern'),
    url(r'^patterns/(?P<pattern_id>\d+)/attach/$', 'pattern_media',
        name='edit-pattern-media'),
    url(
        r'^patterns/(?P<pattern_id>\d+)/view/email/$', 'view_pattern',
        name='view-pattern'),

    url(r'^add/var/$', 'add_var', name='add-var'),
    url(r'^variables/$', 'var_list', name='var-list'),
    url(r'^edit/var/(?P<var_id>\d+)/$', 'edit_var', name='edit-var'),

    url(
        r'^patterns/attach/(?P<pattern_id>\d+)/$', 'pattern_media',
        name='edit-pattern-media'),

    url(r'^patterns/$', 'patterns', name='patterns'),
    url(r'^list/$', 'feedback_list', name='index'),
    url(r'^(?P<feedback_id>\d+)/$', 'detail', name='edit'),
    url(r'^(?P<feedback_id>\d+)/delete/$', 'delete', name='delete'),
    url(
        r'^patterns/(?P<pattern_id>\d+)/delete/$', 'delete_pattern',
        name='delete-pattern'),
    url(r'^list/delete/$', 'delete_list', name='message-delete'),
)

urlpatterns = patterns(
    '',
    url(r'^feedback/', include(public_urls, namespace='public')),
    url(r'^admin/feedback/', include(admin_urls, namespace='admin')),
)
