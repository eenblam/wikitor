import sqlite3

class Pages(object):
    def __init__(self, db, table):
        self.conn = sqlite3.connect(db)
        s = 'INSERT INTO {}(pageid, title, content) VALUES (?,?,?)'
        self.insert_string = s.format(table)

    def add_page(self, pageid, title, content):
        c = self.conn.cursor()
        try:
            c.execute(self.insert_string, (pageid, title, content))
            conn.commit()
        except sqlite3.OperationalError as err:
            #TODO Could not log, enqueue input for retry?
            print("Could not insert page at pageid {}. Error: "
                    .format(pageid, err))

    def close(self):
        self.conn.close()
