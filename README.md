spicy.feedback
==============

Приложение Django для SpicyCMS. Использует [концепцию реиспользования кода и конфигурации spicy.core](https://github.com/spicycms/spicy.core).

Это простое приложение использует по умолчанию типовые шаблоны и часть логики ``spicy.core.admin``. 

Для запуска необходима версия 1.4.11 - 1.5.12 Django.

Назначение
==========
Модуль предназначен для настройки обратной связи на сайте, позволяет настроить через админку email-уведомления менеджеров, SMS рассылку.

Подключить spicy.feedback к вашему приложению
=============================================
Добавьте spicy.feedback в список приложения ``settings.py``:
```
INSTALLED_APPS = (
    ...
    'spicy.feedback',
    ...
)
```

Подключите бэкенды для email и sms рассылки:
```
#settings.py

FEEDBACK_BACKENDS = (
    'spicy.feedback.backends.email', # backend send email(base)
    'spicy.feedback.backends.sms', # backend send SMS(optional)
    'spicy.feedback.backends.rest', # backend send data to CRM(optional)
)
```

И добавьте в ``urls.py`` путь для модуля spicy.feedback:

urlpatterns = patterns('',
    ...
    url(r'^', include('spicy.feedback.urls', namespace='feedback')),
    ...
)

После этого необходимо выполнить ``manage.py syncdb``, чтобы Django создала таблицы sicy.feedback в базе данных.

Настройка email рассылки
===========================

Настройка sms рассылки
===========================
{TODO: подключение Nexmo, про spicy.feedback.backends.sms}

Настройка рассылки в CMS систему
================================
{TODO: про SpicyCMR, со ссылкой; про spicy.feedback.backends.rest}

Кастомизация spicy.feedback
===========================
Вы можете кастомизировать поведение spicy.feedback, с помощью настроек в ``settings.py``.

Модель отзыва Feedback
----------------------
* CUSTOM_FEEDBACK_FORM
* USE_DEFAULT_FEEDBACK
{TODO кастомная модель, ее подключение}

Настройки модуля
----------------
* FEEDBACK_BACKENDS (+ссылка на source code как пример бэкенда)
* USE_FEEDBACK_CAPTCHA
* EMAIL_MAX_LENGTH
* MESSAGES_PER_MINUTE
* FEEDBACK_PER_PAGE
* SEND_AUTO_RESPONSE_WITHOUT_TIMEOUT
* CREATE_NEW_ACCOUT
* STATUS_TYPE_CHOICES
* PATTERN_TEMPLATES_PATH

