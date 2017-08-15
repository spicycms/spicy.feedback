spicy.feedback
==============

Приложение Django для SpicyCMS. Использует [концепцию реиспользования кода и конфигурации spicy.core](https://github.com/spicycms/spicy.core). Это простое приложение использует по умолчанию типовые шаблоны и часть логики ``spicy.core.admin``, определяет модели отзыва Feedback и шаблона отзыва FeedbackPattern для отслеживания обратной связи на сайте.

Для запуска необходима версия 1.4.11 - 1.5.12 Django.

Назначение
----------
Модуль предназначен для организации обратной связи на сайте, позволяет настроить через админку email-уведомления менеджеров, SMS рассылку, рассылку в SpicyCRM об оставленных отзывах, а также отправку автоматических ответных сообщений пользователям.

Подключить spicy.feedback к вашему приложению
---------------------------------------------
Добавьте spicy.feedback в список приложения ``settings.py``:
```
INSTALLED_APPS = (
    ...
    'spicy.feedback',
    ...
)
```

Подключите бэкенды для email, sms рассылки или рассылки в SpicyCRM:
```
#settings.py

FEEDBACK_BACKENDS = (
    'spicy.feedback.backends.email', # backend send email(base)
    'spicy.feedback.backends.sms', # backend send SMS(optional)
    'spicy.feedback.backends.rest', # backend send data to CRM(optional)
)
```

И добавьте в ``urls.py`` путь для модуля spicy.feedback:
```
urlpatterns = patterns('',
    ...
    url(r'^', include('spicy.feedback.urls', namespace='feedback')),
    ...
)
```

После этого необходимо выполнить ``manage.py syncdb``, чтобы Django создала таблицы sicy.feedback в базе данных.

Шаблонные теги spicy.feedback
-----------------------------
{TODO}

Бэкенды spicy.feedback
----------------------

В модуле spicy.feedback реализованы 3 бэкенда, которые позволяют осуществлять рассылку уведомлений менеджерам по emai, sms и в SpicyCRM{TODO вставить ссылку???}. Вы также можете [переопределить или создать свой бэкенд](./README.md#Бэкенд-рассылки-уведомлений). Каждый из бэкендов определяет свои модели для объекта отзыва Feedback и шаблона отзыва Pattern.

Модель Feedback представляет собой отзывы, которые оставляют пользователи, и реализует метод ``send_report()``, который рассылает уведомления в зависимости от бэкенда - на почту, по sms или в CMR.

Модель Pattern определяет шаблон отзывов, по которому в админке настраивается система обратной связи (указываются email менеджеров, заголовки и тело писем, номера отправки для sms уведомлений и т.п.).

### Email рассылка

Бэкенд [spicy.feedback.backends.email](./src/spicy/feedback/backends/email.py) реализует две модели - отзыв Feedback и шаблон отзыва Pattern. С их помощью в админке настраивается рассылка уведомлений об оставленных отзывах менеджерам и ответные письма пользователям.

Pattern унаследован от [spicy.core.simplepages.abs.EditableTemplateModel](https://github.com/spicycms/spicy.core/blob/8436b2677448cc1cd398fc37d4330edfb8f5170a/src/spicy/core/simplepages/abs.py#L12), поэтому в админке доступно дополнительные поля ``content``, которое позволяет определить сообщение, отправляемое на email пользователям, оставившим отзыв; ``template_name`` - имя html-шаблона, используемого для отправки ответных писем.

Например, вы хотите, чтобы в тексте ответного письма отправлялась благодарность за оставленный отзыв, и цвет шрифта был красным. Для этого нужно создать шаблон обратной связи, указав для него Тело письма (``content``) и переопределить html-шаблон ``spicy.feedback/patterns/default.html``, добавив в него css-стили красного шрифта.

``spicy.feedback/patterns/default.html`` используется email бэкендом по умолчанию. Но вы можете выбирать другой html-шаблон, для этого поместите файл вашего html-шаблона в ``spicy.feedback/patterns/`` и через админку выберите его в поле ``Шаблон письма``. Внутри шаблона будут доступны контекстные переменные ``{{ pattern }}``, ``{{ site }}``, ``{{ LANGUAGE_CODE }}`` и ``{{ body }}``.

### Sms рассылка ИСПОЛЬЗУЕТСЯ ЛИ?!
{TODO: подключение Nexmo, про spicy.feedback.backends.sms}

### Рассылки в CMS систему ИСПОЛЬЗУЕТСЯ ЛИ?!
{TODO: про SpicyCMR, со ссылкой; про spicy.feedback.backends.rest}

Кастомизация spicy.feedback
---------------------------
Вы можете кастомизировать поведение spicy.feedback, с помощью настроек в ``settings.py``.

### Своя модель отзыва Feedback
* CUSTOM_FEEDBACK_FORM
* USE_DEFAULT_FEEDBACK
{TODO кастомная модель, ее подключение}

### Свой бэкенд рассылки уведомлений
* FEEDBACK_BACKENDS (+ссылка на source code как пример бэкенда)
{TODO пример кастомизации}

### Дополнительные настройки модуля
* USE_FEEDBACK_CAPTCHA
* EMAIL_MAX_LENGTH
* MESSAGES_PER_MINUTE
* FEEDBACK_PER_PAGE
* SEND_AUTO_RESPONSE_WITHOUT_TIMEOUT
* CREATE_NEW_ACCOUT
* STATUS_TYPE_CHOICES
* PATTERN_TEMPLATES_PATH
