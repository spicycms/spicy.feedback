from django.dispatch import Signal

create_feedback = Signal(providing_args=['request', 'feedback'])
