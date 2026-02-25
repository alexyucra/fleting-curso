from seeds.development import fake_user
def run(db, env="development"):
    # db.execute('''
    #     INSERT OR IGNORE INTO users (username, password)
    #     VALUES ('admin', 'fleting')
    # ''')
    
    # cargamos el archivo fake_users
    if env=="development":
        fake_user.run(db, env, count=20)
