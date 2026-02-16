
def run(db):
    db.execute('''
        INSERT OR IGNORE INTO users (username, password)
        VALUES ('admin', 'fleting')
    ''')
