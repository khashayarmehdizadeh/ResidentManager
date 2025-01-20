import sqlite3
from entity.resident import Resident


class BuildingManager:
    def __init__(self):
        self.conn=sqlite3.connect('building.db')
        self.cursor=self.conn.cursor()
        self.create_table()


        def create_table(self):
            #create a table for residents
            self.cursor,execute('''CREATE TABLE IF NOT EXISTS residents(
                                id TEXT PRIMARY KEY,
                                
                                )''')
        