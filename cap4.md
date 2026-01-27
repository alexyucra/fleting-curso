# 🧠 Ejercicios Paso a Paso

### 📝 Ejercicio 1

Crear una página llamada `profile` que muestre:

- Título
- Texto descriptivo
- Layout principal

comando CLI: 

```shell
fleting create page profile
```

### 📝 Ejercicio 2

Agregar una propiedad nueva al Model y mostrarla en la View.

📄 models/profile_model.py

```py
class ProfileModel:
    def __init__(self):
        self.username = "Usuario Fleting" # adicionar nueva propiedad
```

📄 controllers/profile_controller.py

```py
class ProfileController: 
    def __init__(self, model):
        self.model = model

    def get_username(self):     # nueva funcion que devolverá propiedad del model
        return self.model.username
```

📄 views/pages/profile_view.py
```py
import flet as ft
from controllers.profile_controller import ProfileController # carga de controller
from views.layouts.main_layout import MainLayout

class ProfileView:
    def __init__(self, page, router):
        self.page = page
        self.router = router
        self.controller = ProfileController() # inicializa controller

    def render(self):
        content = ft.Column(
            controls=[
                ft.Text("Perfil", size=24, weight=ft.FontWeight.BOLD),
                ft.Text(f"Usuário: {self.controller.get_username()}"), # imprime propiedad del controller
            ],
            spacing=16,
        )

        return MainLayout(
            page=self.page,
            content=content,
            router=self.router,
        )
```


### 📝 Ejercicio 3

Verificar o Registrar la nueva página en el Router y navegar hacia ella desde otra vista.


📄 configs/routes.py
```py
ROUTE_MAP = {
    "/profile": "views.pages.profile_view.ProfileView", # adicione esta ruta
    "/": "views.pages.home_view.HomeView",
}
```


