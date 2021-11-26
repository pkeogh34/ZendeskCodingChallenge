from datetime import datetime
import json
import requests

from Ticket import Ticket


class Data:

    def __init__(self, url, url_headers):
        self.url = url
        self.url_headers = url_headers
        self.data = {}

    # function to get json data from the Zendesk API
    def fetch(self):
        i = 1
        # holds data for each page that is fetched
        pages = {}
        # fetch the pages
        while True:
            # GET request
            response = requests.get(self.url, headers=self.url_headers)
            jdata = response.text
            data = json.loads(jdata)
            pages[i] = data["results"]
            # if there is no next page
            if data["next_page"] is None:
                break
            i += 1
            # update url to next page
            self.url = data["next_page"]
        return pages

    def parse_raw_data(self, data):
        t_data = {}
        # iterate through each page
        for page in data:
            # parse each type of ticket data
            for obs in data[page]:
                ticket_id = obs["id"]
                created = datetime.strptime(obs["created_at"][:19], "%Y-%m-%dT%H:%M:%S")
                updated = datetime.strptime(obs["updated_at"][:19], "%Y-%m-%dT%H:%M:%S")
                if obs["type"] == "null":
                    ticket_type = "Ticket"
                else:
                    ticket_type = obs["type"]
                subject = obs["subject"]
                status = obs["status"]
                description = obs["description"]
                tags = obs["tags"]
                requester_id = obs["requester_id"]
                ticket = Ticket(ticket_id, created, updated, ticket_type, subject, description, status, tags,
                                requester_id)
                t_data[ticket.ticket_id - 1] = ticket
        return t_data

    def fetch_and_parse_data(self):
        data = self.fetch()
        self.data = self.parse_raw_data(data)

