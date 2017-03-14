Spicy Django Feedback
==============================

Require Django versions: 1.4.11 - 1.5.12

Installation
============

To install the ``spicy.feedback`` package, simply place it anywhere on your
``PYTHONPATH``.

Project settings
----------------

::

    INSTALLED_APPS = (
        ...
        'spicy.feedback',
        ...
    )

    FEEDBACK_BACKENDS = (
        'spicy.feedback.backends.email', # backend send email(base)
        'spicy.feedback.backends.sms', # backend send SMS(optional)
        'spicy.feedback.backends.rest', # backend send data to CRM(optional)
    )

Customazation Feedback to settings.py
-------------------------------------

::

    USE_DEFAULT_FEEDBACK = False
    CUSTOM_FEEDBACK_MODEL = 'apps.webapp.NewFeedbackModel'
    CUSTOM_FEEDBACK_FORM = 'apps.webapp.forms.NewFeedbackForm'

URL Configuration
-----------------

::

    urlpatterns = patterns('',
        ...
        url(r'^', include('spicy.feedback.urls', namespace='feedback')),
        ...
    )


syncdb
------

You must perform ``syncdb`` before using any ``FB`` in ``setting.py``
because we need database table before we can use ``FB``

version
===========================

1.1.0 - latest release
