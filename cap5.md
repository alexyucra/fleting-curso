# 🧠 Ejercicio práctico paso a paso

## 1️⃣ Inicializar el módulo de base de datos:

Comando CLI:

```shell
# inicializa database, prepara archivos prontos de muestra para migracion e seeder
fleting db init

# ejecuta la migracion inicial
fleting db migrate
```

```py
# verifica migrations/001_initial.py
def up(db):
    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
```

```py
# verifica seeds/initial.py
def run(db):
    db.execute('''
        INSERT OR IGNORE INTO users (username, password)
        VALUES ('admin', 'fleting')
    ''')

```

### 2️⃣ Verificar estructura creada:

data/
migrations/
seeds/


### 3️⃣ Abrir data/fleting.db con un visualizador SQLite

puedes usar : `SQLite Viewer`

### 4️⃣ Analizar el archivo:

fleting/core/database.py
