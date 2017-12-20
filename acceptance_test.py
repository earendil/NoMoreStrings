from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_there_is_a_page(self):

        # Load the browser
        self.browser.get('http://localhost:8000')

        # There's a webpage being served with the title NoMoreStrings
        self.assertIn('NoMoreStrings', self.browser.title)


if __name__ == '__main__':
    unittest.main()
