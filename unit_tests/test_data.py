import unittest
import Data


class MyTestCase(unittest.TestCase):
    encoded = "cGF0cmljay5rZW9naDFAdWNkY29ubmVjdC5pZS90b2tlbjp1a05KSlVBaFRiMzRoMmZZejVuVTNGcVdEN2NTSWh1MEd5dENLQm1T"
    headers = {'Content-Type': 'application/json', 'Authorization': 'Basic %s' % encoded}
    url = "https://zcczendeskcodingchallenge6845.zendesk.com/api/v2/search.json?query=type%3Aticket&sort_by" \
          "=created_at&sort_order=asc"
    data_obj = Data.Data(url, headers)
    fetch_data = data_obj.fetch()

    def test_fetch(self):
        self.assertEqual(type({}), type(self.fetch_data))
        self.assertEqual(2, len(self.fetch_data))

    def test_parse_raw_data(self):
        self.assertEqual(type({}), type(self.data_obj.parse_raw_data(self.fetch_data)))
        self.assertEqual(101, len(self.data_obj.parse_raw_data(self.fetch_data)))


if __name__ == '__main__':
    unittest.main()
