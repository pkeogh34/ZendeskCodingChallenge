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
        # fetch the page
        response = requests.get(self.url, headers=self.url_headers)
        jdata = response.text
        return json.loads(jdata)

    def parse_raw_data(self, data):
        t_data = {}
        for obs in data["results"]:
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
            ticket = Ticket(ticket_id, created, updated, ticket_type, subject, description, status, tags, requester_id)
            t_data[ticket.ticket_id-1] = ticket
        self.data = t_data

    def fetch_and_parse_data(self):
        data = self.fetch()
        self.parse_raw_data(data)
