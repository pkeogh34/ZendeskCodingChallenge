import json, requests
from urllib.parse import urlencode

subdomain = "zcczendeskcodingchallenge6845"
encoded = "cGF0cmljay5rZW9naDFAdWNkY29ubmVjdC5pZS90b2tlbjp1a05KSlVBaFRiMzRoMmZZejVuVTNGcVdEN2NTSWh1MEd5dENLQm1T"
url_prefix = "https://%s.zendesk.com/api/v2/search.json" % subdomain
url_headers = {'Content-Type': 'application/json', 'Authorization': 'Basic %s' % encoded}
parameters = {'query': 'type:ticket', 'sort_by': 'created_at', 'sort_order': 'asc'}


# function to get json data from the Zendesk API
def fetch(url, params={}):
    # construct the url
    url += "?" + urlencode(params)
    print("Getting tickets from %s" % url)
    # fetch the page
    response = requests.get(url, headers=url_headers)
    jdata = response.text
    return json.loads(jdata)


fetch(url_prefix, parameters)

