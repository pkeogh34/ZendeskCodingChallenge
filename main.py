from tkinter import WORD, INSERT, RIGHT, Y, LEFT
from urllib.parse import urlencode
import tkinter as tk

from Data import Data

subdomain = "zcczendeskcodingchallenge6845"
encoded = "cGF0cmljay5rZW9naDFAdWNkY29ubmVjdC5pZS90b2tlbjp1a05KSlVBaFRiMzRoMmZZejVuVTNGcVdEN2NTSWh1MEd5dENLQm1T"
url_prefix = "https://%s.zendesk.com/api/v2/search.json" % subdomain
url_headers = {'Content-Type': 'application/json', 'Authorization': 'Basic %s' % encoded}
parameters = {'query': 'type:ticket', 'sort_by': 'created_at', 'sort_order': 'asc'}
ticket_data = {}
w_width = 700
w_height = 450


def get_url(url, params={}):
    url += "?" + urlencode(params)
    return url


def centre_window(window, width, height):
    display_width = window.winfo_screenwidth()
    display_height = window.winfo_screenheight()
    x = (display_width / 2) - (width / 2)
    y = (display_height / 2) - (height / 2)
    window.geometry("{}x{}+{}+{}".format(width, height, int(x), int(y)))


root = tk.Tk()
root.geometry("%dx%d" % (w_width, w_height))
root.resizable(False, False)
centre_window(root, w_width, w_height)
title_frame = tk.Frame(master=root)
title_lbl = tk.Label(
    master=title_frame,
    text="Ticket Viewer",
    font=('Helvetica bold', 35)
)
title_lbl.grid()
title_frame.pack()

root.mainloop()
