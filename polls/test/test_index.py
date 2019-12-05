import datetime

from django.urls import reverse
from django.test import TestCase
from polls.models import Question
from django.utils import timezone

# Create your tests here.


def create_question(question_text, days):
    # create a question and publish the given number of days.
    # Questions yet to be published should not be on the list
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTest(TestCase):
    def test_no_question(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question(self):
        create_question(question_text="Future question", days= 30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        create_question(question_text="past question", days= -30)
        create_question(question_text="Future question", days= 30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: past question>'])


    def test_two_past_questions(self):
        # The question index page may display multiple questions
        create_question(question_text="past question 1", days=-30)
        create_question(question_text="past question 2", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
                                response.context
                                 ['latest_question_list'],
                                 ['<Question: past question 2>',
                                '<Question: past question 1>']
                                 )