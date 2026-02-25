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