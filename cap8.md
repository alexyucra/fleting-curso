# 🧠 Ejercicios Paso a Paso

## 🎯 Ejercicio 1 — Generar todos los models

1. Ejecutar migrations:
```bash
fleting db migrate
```

2. Generar models:
```bash
fleting db model pull
```

3. Verificar carpeta:

```
models/
 ├─ users_model.py
 ├─ roles_model.py
 ├─ posts_model.py
 ├─ categories_model.py
 └─ comments_model.py
```

---

## 🎯 Ejercicio 2 — Generar solo una tabla

```bash
fleting db model pull posts
```

Verificar que solo se actualizó `posts_model.py`.

---

## 🎯 Ejercicio 3 — Forzar actualización

1. Agregar una columna en migration
2. Ejecutar:

```bash
fleting db migrate
fleting db model pull users --force
```

3. Verificar que el model refleja la nueva columna