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


def blue_text(event=None):
    lab.config(fg="blue")


def black_text(event=None):
    lab.config(fg="black")


def get_data(prefix, headers, params={}) -> object:
    data = Data(get_url(prefix, params), headers)
    data.fetch_and_parse_data()
    return data.data


def get_data_helper(event=None):
    global ticket_data
    ticket_data = get_data(url_prefix, url_headers, parameters)
    ticket_frame.destroy()


def open_ticket(num, event=None):
    global ticket_data
    ticket_root = tk.Tk()
    text = tk.Text(ticket_root, wrap=WORD)
    text.insert(INSERT, "Subject: %s\n\n" % ticket_data[num].subject)
    text.insert(INSERT, "Date created: %s\n" % ticket_data[num].created)
    text.insert(INSERT, "Last updated: %s\n\n" % ticket_data[num].updated)
    text.insert(INSERT, "Requester ID: %s\n" % ticket_data[num].requester_id)
    text.insert(INSERT, "Status: %s\n\n" % ticket_data[num].status)
    text.insert(INSERT, ticket_data[num].description)
    text.config(state='disabled')
    text.grid()
    ticket_root.mainloop()


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

ticket_frame = tk.Frame(master=root)

lab = tk.Label(
    master=ticket_frame,
    text="Click here to load ticket data from '%s.zendesk.com'" % subdomain,
    font=('Helvetica', 12)
)
lab.bind("<Button-1>", get_data_helper)
lab.bind("<Enter>", blue_text)
lab.bind("<Leave>", black_text)
lab.pack()

ticket_frame.pack()
root.wait_window(lab)
ticket_frame = tk.Frame(master=root)
root.mainloop()
