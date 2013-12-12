import datetime
from datetime import timedelta
from django.utils.timezone import utc
from django.core.management.base import BaseCommand, CommandError



class Command(BaseCommand):
    help = 'Processes feedback auto response mailing'

    def handle(self, *args, **options):

        from spicy.utils.models import get_custom_model_class
        from spicy.feedback import defaults
            
        Feedback = get_custom_model_class(defaults.CUSTOM_FEEDBACK_MODEL)            
        from spicy.utils.printing import print_error, print_info, print_warning


        now = datetime.datetime.utcnow().replace(tzinfo=utc)

        feedback_timeout = Feedback.objects.filter(
            pattern__isnull=False,
            email_has_been_sent=False,            
        ).distinct('email').order_by('email', '-submit_date').values_list(
            'id', 'pattern__auto_response_timeout')

        feedbacks = []
        
        for id, timeout in feedback_timeout:
            feedbacks.append(
                Feedback.objects.filter(pk=id, submit_date__lte = now - timedelta(minutes=timeout))
                )

        if not feedbacks:
            print_info('Has no new auto feedbacks')
        else:
            totalCount = len(feedbacks)
            sentCount = 0

            print_info('Sending\r\n')
            for feedback in feedbacks[:defaults.MESSAGES_PER_MINUTE]:
                try:
                    print_info('%s\r\n' % feedback.email)
                    feedback.send_using_pattern()
                    sentCount += 1
                except Exception as e:
                    print_error('Error sending to %s: "%s"\r\n' % (feedback.email, str(e)))

            print_info('Total to send: %i\r\nSuccessfully sent: %i\r\n' % (totalCount, sentCount))
