from spicy.utils.models import get_custom_model_class


Feedback = get_custom_model_class(defaults.CUSTOM_FEEDBACK_MODEL)


@receiver(post_save, sender=Feedback)
def save_same(sender, instance, **kwargs):
    if instance.email_has_been_sent == True:
        same_feedbacks = Feedback.objects.filter(
            email=instance.email, type=instance.type, 
            email_has_been_sent=False)

        if same_feedbacks:
            for feedback in same_feedbacks:
                feedback.email_has_been_sent = True
                feedback.save()
