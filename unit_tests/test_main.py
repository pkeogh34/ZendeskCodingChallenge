import unittest

import main as m


class MyTestCase(unittest.TestCase):
    url_prefix = m.url_prefix
    parameters = m.parameters
    headers = m.url_headers
    url = "https://zcczendeskcodingchallenge6845.zendesk.com/api/v2/search.json?query=type%3Aticket&sort_by" \
          "=created_at&sort_order=asc"

    def test_get_url(self):
        self.assertEqual(m.get_url(self.url_prefix, self.parameters), self.url)
        self.assertEqual(type(m.get_url(self.url_prefix, self.parameters)), type(""))

    def test_get_data(self):
        self.assertEqual(type(m.get_data(self.url_prefix, self.headers, self.parameters)), type({}))


if __name__ == '__main__':
    unittest.main()
