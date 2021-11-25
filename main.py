import _tkinter
from json import JSONDecodeError
from tkinter import WORD, INSERT, END
from urllib.parse import urlencode
import tkinter as tk

from requests.exceptions import InvalidSchema, MissingSchema
from Data import Data

# Subdomain for my Zendesk agent
subdomain = "zcczendeskcodingchallenge6845"
# String encoded with email and api key
encoded = "cGF0cmljay5rZW9naDFAdWNkY29ubmVjdC5pZS90b2tlbjp1a05KSlVBaFRiMzRoMmZZejVuVTNGcVdEN2NTSWh1MEd5dENLQm1T"
# prefix of the Zendesk API website
url_prefix = "https://%s.zendesk.com/api/v2/search.json" % subdomain
# Headers to send with get request
url_headers = {'Content-Type': 'application/json', 'Authorization': 'Basic %s' % encoded}
# Parameters to send with get request
parameters = {'query': 'type:ticket', 'sort_by': 'created_at', 'sort_order': 'asc'}
# Dictionary to hold data from API
ticket_data = {}
# Window dimensions
w_width = 700
w_height = 450


# Function that creates the url for GET request
def get_url(url, params):
    # construct url
    url += "?" + urlencode(params)
    return url


# Function that closes the window
def close_window(event=None):
    root.destroy()


# Function to get data from API
def get_data(prefix, headers, params) -> object:
    data = Data(get_url(prefix, params), headers)
    data.fetch_and_parse_data()
    return data.data


# Function used to define button click event
def get_data_helper(event=None):
    global ticket_data, ticket_frame
    # try...except statement to handle errors in obtained data from the API
    try:
        # getting data from the API
        ticket_data = get_data(url_prefix, url_headers, parameters)
    # url is invalid
    except MissingSchema:
        error_button("Could not connect to API")
        return
    except InvalidSchema:
        error_button("Could not connect to API")
        return
    # no data was received from the API
    except KeyError:
        error_button("Did not receive any data from API")
        return
    except JSONDecodeError:
        error_button("Did not receive any data from API")
        return
    ticket_frame.destroy()


def error_button(msg):
    global ticket_data, ticket_frame
    ticket_frame.destroy()
    ticket_frame = tk.Frame(master=root)
    error = tk.Label(master=ticket_frame, text=msg, pady=5, font=('Helvetica bold', 16))
    error.pack()
    btn = tk.Button(master=ticket_frame, text="Exit", pady=5, width=5)
    btn.bind('<Button-1>', close_window)
    btn.pack()
    ticket_frame.pack()


# Functions to define an event to change text colour
def blue_text(event=None):
    lbl.config(fg="purple")


def black_text(event=None):
    lbl.config(fg="blue")


# Function to centre window on the screen
def centre_window(window, width, height):
    display_width = window.winfo_screenwidth()
    display_height = window.winfo_screenheight()
    x = (display_width / 2) - (width / 2)
    y = (display_height / 2) - (height / 2)
    window.geometry("{}x{}+{}+{}".format(width, height, int(x), int(y)))


# Function that creates a new window and display ticket data
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
    tags = ""
    for tag in ticket_data[num].tags:
        tags += "#%s" % tag
    text.insert(END, tags)
    text.config(state='disabled')
    text.grid()
    ticket_root.mainloop()


# Function that defines an event to create the buttons on the window
def create_buttons():
    # create a canvas and scrollbar in order to scroll through displayed tickets
    canvas = tk.Canvas(ticket_frame)
    scrollbar = tk.Scrollbar(ticket_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # for loop that creates buttons necessary to open tickets
    for i in range(25):
        if (i + j) < len(ticket_data):
            ticket_btn = tk.Button(master=scrollable_frame, text=ticket_data[i + j].subject, width=100)

            # create a function that defines an open_ticket event specific to current (i) ticket
            def handler(event, num=i + j):
                return open_ticket(num, event)

            ticket_btn.bind('<Button-1>', handler)
            ticket_btn.pack(fill="both", expand=True)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # decide which buttons to display for pagination
    if j >= 0 and ((j + 25) < len(ticket_data)):
        btn = tk.Button(master=pagination_frame, text="next")
        btn.bind('<Button-1>', next_page)
        btn.pack(side="right")
    if j > 0:
        btn = tk.Button(master=pagination_frame, text="previous")
        btn.bind('<Button-1>', previous_page)
        btn.pack(side="left")

    # display buttons on the window
    ticket_frame.pack(fill="both", expand=True)
    pagination_frame.pack()


# Function that defines event to change to the next page
def next_page(event=None):
    global j, ticket_frame, pagination_frame
    j += 25
    refresh()
    create_buttons()


# Function that defines event to return to the previous page
def previous_page(event=None):
    global j, ticket_frame, pagination_frame
    j -= 25
    refresh()
    create_buttons()


# Function to refresh window after changing page
def refresh():
    global ticket_frame, pagination_frame
    ticket_frame.destroy()
    pagination_frame.destroy()
    ticket_frame = tk.Frame(master=root)
    pagination_frame = tk.Frame(master=root, pady=7)


# declare the main root window
root = tk.Tk()
root.geometry("%dx%d" % (w_width, w_height))
root.resizable(False, False)
centre_window(root, w_width, w_height)

# declare frame to hold window title
title_frame = tk.Frame(master=root)
title_lbl = tk.Label(
    master=title_frame,
    text="Ticket Viewer",
    font=('Helvetica bold', 35)
)
title_lbl.grid()
title_frame.pack()

# declare frame that will hold the buttons to open tickets
ticket_frame = tk.Frame(master=root)
lbl = tk.Label(
    master=ticket_frame,
    text="Click here to load ticket data from '%s.zendesk.com'" % subdomain,
    font=('Helvetica', 12)
)
# binds the text to change colour when under cursor
lbl.bind("<Button-1>", get_data_helper)
lbl.bind("<Enter>", blue_text)
lbl.bind("<Leave>", black_text)
lbl.pack()

# display widgets on the window
ticket_frame.pack()
# wait for user to request data
root.wait_window(lbl)

# handles error if window is closed before data is requested
try:
    # create frames for ticket buttons and pagination buttons
    ticket_frame = tk.Frame(master=root)
    pagination_frame = tk.Frame(master=root, pady=7)

    j = 0
# create the initial ticket buttons
    create_buttons()
except _tkinter.TclError:
    pass
# main loop for window
root.mainloop()
