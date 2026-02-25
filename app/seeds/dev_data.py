# seeds/dev_data.py  
def run(db, env="development"):

    if env != "development":
        print("⚠️ Seed DEV ignorado fora do ambiente development")
        return

    # Criar admin de desenvolvimento
    db.execute("""
        INSERT OR IGNORE INTO users
        (username, email, password_hash, role_id, is_active, is_verified)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        "dev_admin",
        "admin@dev.local",
        "hashed_password_dev",
        1,
        1,
        1
    ))

    # Criar posts de exemplo
    posts = [
        (1, 1, "Bem-vindo ao Fleting", "bem-vindo-ao-fleting", "Conteúdo inicial...", "published"),
        (1, 2, "Como usar migrations", "como-usar-migrations", "Guia completa...", "draft"),
    ]
    db.execute("DELETE FROM posts")
    db.executemany("""
        INSERT INTO posts
        (user_id, category_id, title, slug, content, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, posts)

    print("👥 Usuário dev + posts criados")