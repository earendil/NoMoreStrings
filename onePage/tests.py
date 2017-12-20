from django.test import TestCase


# Create your tests here.
class HomePageTest(TestCase):

    def test_homepage_for_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'index.html')
