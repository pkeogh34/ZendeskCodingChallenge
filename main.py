from tkinter import WORD, INSERT
from urllib.parse import urlencode
try:
    import Tkinter as tkinter
    import tk
except:
    import tkinter as tk

from requests.exceptions import InvalidSchema

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


def close_window(event=None):
    root.destroy()


def get_data(prefix, headers, params={}) -> object:
    data = Data(get_url(prefix, params), headers)
    data.fetch_and_parse_data()
    return data.data


def get_data_helper(event=None):
    global ticket_data, ticket_frame
    try:
        ticket_data = get_data(url_prefix, url_headers, parameters)
    except InvalidSchema:
        ticket_frame.destroy()
        ticket_frame = tk.Frame(master=root)
        error = tk.Label(master=ticket_frame, text="Could not connect to API", pady=5, font=('Helvetica bold', 16))
        error.pack()
        btn = tk.Button(master=ticket_frame, text="Exit", pady=5, width=5)
        btn.bind('<Button-1>', close_window)
        btn.pack()
        ticket_frame.pack()
        return
    except KeyError:
        ticket_frame.destroy()
        ticket_frame = tk.Frame(master=root)
        error = tk.Label(master=ticket_frame, text="Did not receive any data from API", pady=5, font=('Helvetica bold', 16))
        error.pack()
        btn = tk.Button(master=ticket_frame, text="Exit", pady=5, width=5)
        btn.bind('<Button-1>', close_window)
        btn.pack()
        ticket_frame.pack()
        return
    ticket_frame.destroy()


def blue_text(event=None):
    lab.config(fg="purple")


def black_text(event=None):
    lab.config(fg="blue")


def centre_window(window, width, height):
    display_width = window.winfo_screenwidth()
    display_height = window.winfo_screenheight()
    x = (display_width / 2) - (width / 2)
    y = (display_height / 2) - (height / 2)
    window.geometry("{}x{}+{}+{}".format(width, height, int(x), int(y)))


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


def create_buttons():
    canvas = tk.Canvas(ticket_frame)
    scrollbar = tk.Scrollbar(ticket_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    for i in range(25):
        if (i + j) < len(ticket_data):
            ticket_btn = tk.Button(master=scrollable_frame, text=ticket_data[i + j].subject, width=100)

            def handler(event, num=i + j):
                return open_ticket(num, event)

            ticket_btn.bind('<Button-1>', handler)
            ticket_btn.pack(fill="both", expand=True)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    if j >= 0 and ((j + 25) < len(ticket_data)):
        btn = tk.Button(master=pagination_frame, text="next")
        btn.bind('<Button-1>', next_page)
        btn.pack(side="right")
    if j > 0:
        btn = tk.Button(master=pagination_frame, text="previous")
        btn.bind('<Button-1>', previous_page)
        btn.pack(side="left")

    ticket_frame.pack(fill="both", expand=True)
    pagination_frame.pack()


def next_page(event=None):
    global j, ticket_frame, pagination_frame
    j += 25
    refresh()
    create_buttons()


def previous_page(event=None):
    global j, ticket_frame, pagination_frame
    j -= 25
    refresh()
    create_buttons()


def refresh():
    global ticket_frame, pagination_frame
    ticket_frame.destroy()
    pagination_frame.destroy()
    ticket_frame = tk.Frame(master=root)
    pagination_frame = tk.Frame(master=root, pady=7)


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
pagination_frame = tk.Frame(master=root, pady=7)

j = 0
create_buttons()
root.mainloop()
