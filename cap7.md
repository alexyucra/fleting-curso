## 🧠 Exercício Prático: Sistema de Blog com Seeds
En este ejercicio, aprenderás a poblar tu base de datos de forma modular. Dividiremos los datos en tres niveles: Críticos (Roles/Categorías), Desarrollo (Posts fijos) y Testing (Usuarios aleatorios).

Requisitos: capitulo 6

```shell
fleting db init     # inicializa db
fleting db migrate  # 
fleting db status   # verifica status de las migraciones
```

Estructura organizada:
Organiza tus archivos en la carpeta seeds/ para mantener la lógica separada:

```shell
seeds/
├── initial.py              # Orquestador principal (el que ejecuta todo)
├── essential_data.py       # Datos CRÍTICOS (Roles y Categorías)
├── dev_data.py             # Datos de prueba (Admin y Posts fijos)
└── development/
    └── fake_users.py       # Generador de volumen (Usuarios aleatorios)
```


### 1️⃣ Este archivo `seedes/initial.py` 
es el punto de entrada. aqui debes importar los demás módulos y decidir qué ejecutar según el ambiente (development o production). 

edita el archivo debe quedarte asi:

```py
from seeds.development import fake_users

def run(db, env="development"):
    # db.execute('''
    #     INSERT OR IGNORE INTO users (username, password)
    #     VALUES ('admin', 'fleting')
    # ''')
    
    # Ejecuta los 20 usuarios fake, cargamos el archivo fake_users
    if env == "development":
        fake_users.run(db, env, count=20)
```

### 2️⃣ Datos Críticos: seeds/essential_data.py

Define la estructura mínima para que el sistema funcione. Usamos INSERT OR IGNORE para que, si vuelves a ejecutar el comando, los datos no se dupliquen ni generen errores.

```py
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
```

Agora usamos dados fake apenas para DEV.
### 3️⃣ Datos de Desarrollo: seeds/dev_data.py

Aquí creamos contenido para "ver" algo en el blog mientras programamos.

Nota: Usamos DELETE FROM posts antes de insertar para limpiar la mesa y tener siempre los mismos posts de prueba sin conflictos de slug único.

```py
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
```
### 4️⃣ Volumen de Datos: seeds/development/fake_users.py

Este script utiliza la librería Faker (si está instalada) para crear usuarios realistas masivamente. Es ideal para probar paginación y rendimiento.

```py
# seeds/development/fake_users.py
import random
import re
from datetime import datetime, timedelta
try:
    from faker import Faker
    HAS_FAKER = True
except ImportError:
    HAS_FAKER = False

def slugify(text):
    """Útil para generar usernames o slugs"""
    return re.sub(r'[\s/]', '-', re.sub(r'[^\w\s-]', '', text.lower()))

def run(db, env="development", count=20):
    """Cria usuários fake usando comandos directos de DB"""
    
    print(f"🚀 Iniciando seed de usuarios (Ambiente: {env})")

    # 1. Crear Admin de desarrollo (Usando INSERT OR IGNORE para evitar el error de UNIQUE)
    admin_data = (
        "dev_admin",
        "admin@dev.local",
        "$2b$12$FakeHashForDevOnly1234567890", # pass: dev123
        1, # role_id
        1, # is_active
        1  # is_verified
    )

    db.execute("""
        INSERT OR IGNORE INTO users (username, email, password_hash, role_id, is_active, is_verified)
        VALUES (?, ?, ?, ?, ?, ?)
    """, admin_data)

    # 2. Generar usuarios fake
    if env == "development" and count > 0:
        if HAS_FAKER:
            fake = Faker("pt_BR")
            print("✅ Usando Faker para datos reales")
        else:
            print("ℹ️ Faker no instalado, usando datos estáticos")
            names = ["Ana Silva", "Carlos Souza", "Mariana Lima", "Pedro Rocha"]

        users_created = 0
        for i in range(count):
            if HAS_FAKER:
                full_name = fake.name()
                email = fake.email()
            else:
                full_name = random.choice(names) + f" {i}"
                email = f"user{i}@example.local"

            username = f"user_{i+1:03d}"
            
            # Insertamos con OR IGNORE para que si el email se repite, no se detenga el script
            try:
                db.execute("""
                    INSERT OR IGNORE INTO users 
                    (username, email, password_hash, role_id, is_active, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    username, 
                    email, 
                    f"hash_{i}", 
                    random.choice([2, 3]), # Editor o User
                    1, 
                    datetime.now() - timedelta(days=random.randint(0, 30))
                ))
                users_created += 1
            except Exception as e:
                print(f"❌ Error insertando usuario {i}: {e}")

        print(f"👥 Proceso terminado. Intento de creación: {users_created} usuarios")

    # 3. Estadísticas finales
    cursor = db.execute("SELECT COUNT(*) FROM users")
    total = cursor.fetchone()[0]
    print(f"📊 Total de usuarios actuales en la base: {total}")
```
### 🚀 Ejecución
Una vez configurado todo, simplemente abre tu terminal y ejecuta:

ejecute el comando:

```shell
fleting db seed
```

### El comando fleting shell

El comando fleting shell es una de las herramientas más potentes del framework. Abre una consola interactiva de Python preconfigurada que te permite interactuar con tu base de datos en tiempo real, sin tener que escribir scripts ni usar herramientas externas como DB Browser for SQLite.

Aquí tienes la explicación detallada de lo que hiciste en tu sesión:

1. fleting shell (El Entorno)
Al ejecutarlo, Fleting detecta tu base de datos y te ofrece "helpers" (atajos). No es solo una terminal de Python; tiene superpoderes para mostrar datos de forma visual.

2. tables()
Este comando lista todas las tablas existentes en tu base de datos actual.

_fleting_migrations: Controla qué migrations se han aplicado.

sqlite_sequence: Interna de SQLite para manejar los AUTOINCREMENT.

users, roles, etc.: Las tablas que creaste en tus archivos de migration.

3. table('nombre_tabla')
Es un helper visual. En lugar de devolverte una lista cruda de datos, genera una tabla formateada en la consola.

En users: Viste al dev_admin y a los usuarios con hash_0, hash_1, etc. Esto confirma que tu script fake_users.py funcionó correctamente.

En roles: Confirmaste que los roles (admin, editor, user) tienen los IDs y permisos correctos.

En categories: Verificaste que los datos de essential_data.py se insertaron bien.

4. table('comments') → "Table exists but has no records"
Este mensaje es muy útil. Te indica que:

La estructura está bien: La tabla fue creada por la migration.

Está vacía: Aún no has ejecutado ningún seed que cree comentarios, o no hay interacciones en el sistema.