## 🧠 Ejercicio práctico paso a paso

```shell
# 1️⃣ iniciar estructura de banco de dados
fleting db init

# 2️⃣ Crear nueva migracion
fleting db make create_posts

#' edita los archivos de migración'
```

## Ejercicios: 💻 Código Base Mejorado con Casos Reales

📄 migrations/001_initial.py (Completo y Comentado)

aqui tenemos 2 caminos :
1. El Camino Limpio: Modificar la migración inicial `migrations/001_initial.py` 
2. Crear una segunda migración (ALTER TABLE) - caso real

para efectos del curso usaremos el primero camino: haz este cambio antes de aplicar la migracion.
```py
"""
Migration: 001_initial.py
Autor: Tu Nombre
Fecha: 2026-01-15
Descripción: Crea la tabla inicial de usuarios del sistema
"""

def up(db):
    """
    Ejecuta los cambios FORWARD en la base de datos.
    Se llama al aplicar la migration.
    """
    # 1. Tabla principal de usuarios
    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            
            -- Datos de autenticación
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            
            -- Estado y permisos
            is_active BOOLEAN DEFAULT 1,
            is_verified BOOLEAN DEFAULT 0,
            role_id INTEGER DEFAULT 1,
            
            -- Metadatos
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login_at TIMESTAMP NULL,
            
            -- Restricciones explícitas
            CHECK (LENGTH(username) >= 3),
            CHECK (email LIKE '%@%')
        )
    ''')
    
    # 2. Índices para mejor rendimiento
    db.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)')
    db.execute('CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)')
    db.execute('CREATE INDEX IF NOT EXISTS idx_users_role ON users(role_id)')
    
    # 3. Tabla de roles (relacionada)
    db.execute('''
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY,
            name VARCHAR(30) UNIQUE NOT NULL,
            permissions TEXT DEFAULT '[]',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    print("""
Migration 001 aplicada exitosamente:
   - Tabla 'users' creada (6 campos + 3 índices)
   - Tabla 'roles' creada con 3 roles base
   - Índices optimizados para búsquedas
    """)

def down(db):
    """
    Ejecuta los cambios BACKWARD (rollback).
    Se llama al revertir la migration.
    
    IMPORTANTE: El orden inverso es crucial
    """
    # 1. Eliminar índices (primero)
    db.execute('DROP INDEX IF EXISTS idx_users_role')
    db.execute('DROP INDEX IF EXISTS idx_users_username')
    db.execute('DROP INDEX IF EXISTS idx_users_email')
    
    # 2. Eliminar datos de roles
    db.execute('DELETE FROM roles WHERE id IN (1, 2, 3)')
    
    # 3. Eliminar tablas (en orden inverso de creación)
    db.execute('DROP TABLE IF EXISTS roles')
    db.execute('DROP TABLE IF EXISTS users')
    
    print("""
Migration 001 revertida completamente:
   - Tablas 'users' y 'roles' eliminadas
   - Todos los índices removidos
   - Ready para recrear desde cero
    """)
```

📄 migrations/002_create_posts.py (Ejemplo de Migration Relacional)

```py
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
```

```shell
# 3️⃣ Ejecutar migrations:
fleting db migrate

# 4️⃣ Verificar archivos en:
migrations/

# 5️⃣ Validar datos insertados en el banco
```

### BONUS: ejemplo de insercion de usuarios por comando interactivo:
para este ejemplo  usaremos el comando interactivo ```fleting shell```

```shell
# iniciar comando interactivo
fleting shell

# insertamos um par de usuarios en el banco
fleting > db.execute("""INSERT INTO users (username, email, password_hash, role_id, is_active, is_verified) VALUES (?, ?, ?, ?, ?, ?)""", ( "admin", "admin@example.com", "hashed_password_admin", 1, 1, 1))

fleting > db.execute("""INSERT INTO users (username, email, password_hash, role_id) VALUES (?, ?, ?, ?)""", (    "john", "john@example.com", "hashed_password_john", 2))

# verificamos las tablas creada en el banco
fleting > tables()
# resultado debe salir algo como esto:
# ['_fleting_migrations', 'sqlite_sequence', 'users', 'roles', 'categories', 'posts', 'comments']

# ahora verificamos la tabla users: 
fleting > table("users")

# no te olvides de comentar en los post del canal!
```
