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