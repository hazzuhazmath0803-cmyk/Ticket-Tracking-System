class Ticket:

    def __init__(self,id,title,description,status,
                 priority,assigned_to,due_date):

        self.id=id
        self.title=title
        self.description=description
        self.status=status
        self.priority=priority
        self.assigned_to=assigned_to
        self.due_date=due_date