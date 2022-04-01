import psycopg2
from psycopg2 import Error


class Database:
    def __init__(self):
        self.conn = psycopg2.connect(user="postgres",
                                        password="postgres",
                                        host="localhost",
                                        port="5432",
                                        database="reports_testing")
        self.cur = self.conn.cursor()

    def close(self):
        self.cur.close()
        self.conn.close()
    
    def select(self, query, bindings = None):
        self.cur.execute(query, bindings)
        return self.cur.fetchone()

    def insert(self, query, bindings = None):
        self.cur.execute(query, bindings)
        self.conn.commit()