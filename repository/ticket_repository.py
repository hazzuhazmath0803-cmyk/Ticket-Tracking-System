from repository.db import get_connection
from domain.ticket import Ticket

class TicketRepository:

    def insert_ticket(self,t):

        conn=get_connection()
        cursor=conn.cursor()

        cursor.execute("""
        INSERT INTO ticket(title,description,status,
        priority,assigned_to,due_date)
        VALUES(%s,%s,%s,%s,%s,%s)
        """,(t.title,t.description,t.status,
             t.priority,t.assigned_to,t.due_date))

        conn.commit()
        cursor.close()
        conn.close()

    def get_all_tickets(self):

        conn=get_connection()
        cursor=conn.cursor()

        cursor.execute("SELECT * FROM ticket")
        rows=cursor.fetchall()

        tickets=[]
        for r in rows:
            tickets.append(
            Ticket(r[0],r[1],r[2],r[3],
                   r[4],r[5],r[6])
            )

        cursor.close()
        conn.close()
        return tickets

    def update_ticket(self,t):

        conn=get_connection()
        cursor=conn.cursor()

        cursor.execute("""
        UPDATE ticket SET
        title=%s,description=%s,status=%s,
        priority=%s,assigned_to=%s,due_date=%s
        WHERE id=%s
        """,(t.title,t.description,t.status,
             t.priority,t.assigned_to,t.due_date,t.id))

        conn.commit()
        cursor.close()
        conn.close()

    def delete_ticket(self,id):

        conn=get_connection()
        cursor=conn.cursor()

        cursor.execute(
        "DELETE FROM ticket WHERE id=%s",(id,))

        conn.commit()
        cursor.close()
        conn.close()

    def get_tickets_by_status(self,status):

        conn=get_connection()
        cursor=conn.cursor()

        cursor.execute(
        "SELECT * FROM ticket WHERE status=%s",
        (status,))

        rows=cursor.fetchall()

        tickets=[]
        for r in rows:
            tickets.append(
            Ticket(r[0],r[1],r[2],r[3],
                   r[4],r[5],r[6])
            )

        cursor.close()
        conn.close()
        return tickets

    def search_ticket(self,title):

        conn=get_connection()
        cursor=conn.cursor()

        cursor.execute("""
        SELECT * FROM ticket
        WHERE title LIKE %s
        """,("%"+title+"%",))

        rows=cursor.fetchall()

        tickets=[]
        for r in rows:
            tickets.append(
            Ticket(r[0],r[1],r[2],r[3],
                   r[4],r[5],r[6])
            )

        cursor.close()
        conn.close()
        return tickets

    def dashboard(self):

        conn=get_connection()
        cursor=conn.cursor()

        cursor.execute("""
        SELECT COUNT(*),
        SUM(status='OPEN'),
        SUM(status='CLOSED'),
        SUM(status='IN_PROGRESS')
        FROM ticket
        """)

        row=cursor.fetchone()

        cursor.close()
        conn.close()

        return {
        "total":row[0],
        "open":row[1] or 0,
        "closed":row[2] or 0,
        "progress":row[3] or 0
        }