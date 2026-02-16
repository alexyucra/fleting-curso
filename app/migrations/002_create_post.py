"""
Migration: 002_create_posts.py
Depende de: 001_create_users.py
Descripción: Sistema de posts/blog con categorías
"""

def up(db):
    # 1. Tabla de categorías
    db.execute('''
        CREATE TABLE categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(50) UNIQUE NOT NULL,
            slug VARCHAR(60) UNIQUE NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 2. Tabla de posts
    db.execute('''
        CREATE TABLE posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category_id INTEGER,
            title VARCHAR(200) NOT NULL,
            slug VARCHAR(220) UNIQUE NOT NULL,
            content TEXT NOT NULL,
            excerpt VARCHAR(300),
            status VARCHAR(20) DEFAULT 'draft',
            view_count INTEGER DEFAULT 0,
            published_at TIMESTAMP NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            -- Claves foráneas
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
            
            -- Restricciones
            CHECK (status IN ('draft', 'published', 'archived'))
        )
    ''')
    
    # 3. Índices para posts
    db.execute('CREATE INDEX idx_posts_user ON posts(user_id)')
    db.execute('CREATE INDEX idx_posts_category ON posts(category_id)')
    db.execute('CREATE INDEX idx_posts_status ON posts(status)')
    db.execute('CREATE INDEX idx_posts_slug ON posts(slug)')
    
    # 4. Tabla de comentarios (relacional)
    db.execute('''
        CREATE TABLE comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            user_id INTEGER,
            author_name VARCHAR(100),
            author_email VARCHAR(150),
            content TEXT NOT NULL,
            is_approved BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
        )
    ''')
    
    print("✅ Sistema de blog creado: posts, categorías y comentarios")

def down(db):
    # Orden inverso IMPORTANTE
    db.execute('DROP TABLE IF EXISTS comments')
    db.execute('DROP INDEX IF EXISTS idx_posts_slug')
    db.execute('DROP INDEX IF EXISTS idx_posts_status')
    db.execute('DROP INDEX IF EXISTS idx_posts_category')
    db.execute('DROP INDEX IF EXISTS idx_posts_user')
    db.execute('DROP TABLE IF EXISTS posts')
    db.execute('DROP TABLE IF EXISTS categories')