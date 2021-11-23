from tkinter import WORD, INSERT
from urllib.parse import urlencode
import tkinter as tk

from Data import Data

subdomain = "zcczendeskcodingchallenge6845"
encoded = "cGF0cmljay5rZW9naDFAdWNkY29ubmVjdC5pZS90b2tlbjp1a05KSlVBaFRiMzRoMmZZejVuVTNGcVdEN2NTSWh1MEd5dENLQm1T"
url_prefix = "https://%s.zendesk.com/api/v2/search.json" % subdomain
url_headers = {'Content-Type': 'application/json', 'Authorization': 'Basic %s' % encoded}
parameters = {'query': 'type:ticket', 'sort_by': 'created_at', 'sort_order': 'asc'}
ticket_data = {}
w_width = 500
w_height = 350

