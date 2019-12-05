import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    # This makes the object readable
    def __str__(self):
        return self.question_text

    # This method checks if the question was recently published
    def was_published_recently(self):
        now = timezone.now()
        # was_published_recently.admin_order_field = 'pub_date'
        # was_published_recently.boolean = True
        # was_published_recently.short_description = 'Published recently'
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    # This makes the object readable
    def __str__(self):
        return self.choice_text