# capitulo 3

## ✅ Ejercicio 1 — Verificar BottomBar

- Verificar _bottom_bar en MainLayout
- Modificar visibilidad de botones según rutas registradas en configs/routes.py
```py
ROUTES = [
    {
        "show_in_top": True,
        "show_in_bottom": True,
    },
```
- Probar navegación entre Home y Settings

## ✅ Ejercicio 2 — Estado global

- Verificar AppState.current_route
- Actualizar initial_device para "desktop"
- cambiar de tamaño de aplicativo en configs/app_configs.py

```py
 DESKTOP = {
        "width": 440, #1280,
        "height": 720, # 800,
        "max_content_width": None,  # no limit
    }
```

```
DEFAULT_SCREEN = ScreenConfig.TABLET # DESKTOP | MOBILE | TABLET
```

## ✅ Ejercicio 3 — Prueba completa

- Crear 3 páginas de prueba (test1, test2, test3), usando el comando: 

```shell
fleting create page test1
fleting create page test2
fleting create page test3
```
- Verificar navegación con TopBar y BottomBar
- Cambiar estado y comprobar que el layout se actualiza dinámicamente

### ✅ Ejercicio 4 — Verificar rutas creadas automáticamente

- verificar ROUTES al crear nuevas páginas configs/routes.py
```py
ROUTES = [
    {
    },
```
- Confirmar que el botón se añade automáticamente al TopBar