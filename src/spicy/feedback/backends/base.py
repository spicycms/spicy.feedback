from django.db import models


class Pattern(models.Model):
    class Meta:
        abstract = True


class Feedback(models.Model):
    def send_report(self):
        pass

    def send_to_clients(self):
        pass

    class Meta:
        abstract = True


admin_form = None
