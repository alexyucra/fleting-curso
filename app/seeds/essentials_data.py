# seeds/essential_data.py
def run(db, env="development"):
    """
    Dados CRÍTICOS para qualquer ambiente.
    """

    # 1️⃣ Criar roles base
    roles = [
        (1, "admin", '["*"]'),
        (2, "editor", '["posts.create","posts.edit"]'),
        (3, "user", '["posts.view"]'),
    ]

    db.executemany(
        "INSERT OR IGNORE INTO roles (id, name, permissions) VALUES (?, ?, ?)",
        roles
    )

    # 2️⃣ Criar categorias iniciais
    categories = [
        ("Tecnologia", "tecnologia", "Posts sobre tecnologia"),
        ("Tutoriais", "tutoriais", "Guias e tutoriais"),
        ("Notícias", "noticias", "Atualizações do sistema"),
    ]

    db.executemany(
        """
        INSERT OR IGNORE INTO categories (name, slug, description)
        VALUES (?, ?, ?)
        """,
        categories
    )

    print(f"✅ Seeds essenciais carregados ({env})")