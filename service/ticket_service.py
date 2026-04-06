from repository.ticket_repository import TicketRepository
from domain.ticket import Ticket

class TicketService:

    def __init__(self):
        self.repo=TicketRepository()

    def create_ticket(self,title,desc,status,
                      priority,assigned,due):

        ticket=Ticket(None,title,desc,status,
                      priority,assigned,due)

        self.repo.insert_ticket(ticket)

    def fetch_all(self):
        return self.repo.get_all_tickets()

    def update_ticket(self,id,title,desc,status,
                      priority,assigned,due):

        ticket=Ticket(id,title,desc,status,
                      priority,assigned,due)

        self.repo.update_ticket(ticket)

    def delete(self,id):
        self.repo.delete_ticket(id)

    def fetch_by_status(self,status):
        return self.repo.get_tickets_by_status(status)

    def search(self,title):
        return self.repo.search_ticket(title)

    def dashboard(self):
        return self.repo.dashboard()