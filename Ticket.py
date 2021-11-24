class Ticket:
    def __init__(self, ticket_id, created, updated, ticket_type,  subject, description, status, tags,
                 requester_id):
        self._ticket_id = ticket_id
        self.created = created
        self.updated = updated
        self.ticket_type = ticket_type
        self.subject = subject
        self.description = description
        self.status = status
        self.tags = tags
        self.requester_id = requester_id

    @property
    def ticket_id(self):
        return self._ticket_id
