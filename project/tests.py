from django.test import TestCase


class ProjectTestCase(TestCase):
    '''
      Dummy test to check the default CI/CD
    '''
    def test_animals_can_speak(self):
        self.assertEqual(1, 1)
