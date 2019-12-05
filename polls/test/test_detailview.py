import datetime

from django.urls import reverse
from django.test import TestCase
from polls.models import Question
from django.utils import timezone

def create_question(question_text, days):
    # create a question and publish the given number of days.
    # Questions yet to be published should not be on the list
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionDetailViewTest(TestCase):
    def test_future_question(self):
        #The detailview of a question with future date returns a 404 not found
        future_question = create_question(question_text='Future question', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    def test_past_question(self):
        #  The detailview of a question in the past displays the question text
        past_question = create_question(question_text="Past question", days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

