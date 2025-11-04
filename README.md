# API de Biblioteca Digital

Sistema de gestión para Biblioteca, Repositorio y Marketplace.

Este proyecto backend está construido con FastAPI y sigue principios de **Arquitectura Limpia (Clean Architecture)** para separar la lógica de negocio del framework y la infraestructura.

## 🚀 Tecnologías Principales

* **Python 3.9+**
* **FastAPI:** Para la creación de la API RESTful.
* **Pydantic:** Para la validación de datos (DTOs y Entidades).
* **SQLAlchemy:** Como ORM para la interacción con la base de datos.
* **PostgreSQL:** Como motor de base de datos.
* **JWT (JSON Web Tokens):** Para la autenticación de usuarios.
* **Docker:** Para la contenedorización de la aplicación.

---

## 🏛️ Arquitectura del Proyecto

El proyecto está dividido en tres capas principales, siguiendo un modelo de Arquitectura Limpia/Hexagonal:

### 1. `dominio/` (Capa de Dominio)

Es el núcleo del sistema. No depende de ninguna otra capa.

* `dominio/entidades/`: Contiene los modelos principales del negocio (ej. `Usuario`, `Libro`, `Alquiler`) definidos con Pydantic.
* `dominio/value_objects/`: Objetos de valor inmutables (ej. `RolUsuario`, `EstadoAlquiler`).
* `dominio/puertos/`: Define las interfaces (Ports) que la capa de aplicación usará, sin conocer la implementación (ej. `IRepoUsuario`, `IRepoLibro`).

### 2. `aplicacion/` (Capa de Aplicación)

Orquesta la lógica de negocio. Depende de la capa de `dominio`.

* `aplicacion/casos_uso/`: Contiene la lógica de negocio específica (ej. `CU_RegistrarUsuario`, `CU_GestionarLibros`). Estos casos de uso interactúan con las interfaces (puertos) del dominio.
* `aplicacion/dto/`: (Data Transfer Objects) Define la estructura de los datos que entran y salen de la API (ej. `UsuarioRegistroDTO`, `LibroCrearDTO`).

### 3. `infraestructura/` (Capa de Infraestructura)

Contiene las implementaciones concretas de las interfaces y todo lo relacionado con herramientas externas (BD, API, etc.). Depende de `aplicacion` y `dominio`.

* `infraestructura/api/`: Define los *endpoints* de FastAPI (routers). Actúa como el "adaptador de entrada" (driving adapter).
    * `auth_router.py`: Maneja el registro (`/register`) y login (`/login`).
    * `libro_router.py`: Maneja el CRUD de libros (`/libros`).
    * `alquiler_router.py`: Maneja la solicitud de préstamos (`/alquiler`).
    * `market_router.py`: Maneja la publicación de productos (`/market`).
* `infraestructura/persistencia/`: Implementa los repositorios (adaptadores de salida) definidos en `dominio/puertos`.
    * `RepositorioUsuarioSQL.py`: Implementación concreta de `IRepoUsuario` usando SQLAlchemy.
    * `RepositorioLibroSQL.py`: Implementación de `IRepoLibro`.
    * `configuracion.py`: Configuración de la sesión y motor de SQLAlchemy.
* `infraestructura/seguridad/`: Implementa la lógica de seguridad.
    * `password_hasher.py`: Lógica para hashear y verificar contraseñas.
    * `ServicioAutenticacionJWT.py`: Lógica para crear y validar tokens JWT.

---

## 🏁 Cómo Empezar

### Prerrequisitos

* Python 3.9 o superior
* PostgreSQL
* Git

### Instalación y Ejecución Local

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/tu-usuario/tu-repositorio.git](https://github.com/tu-usuario/tu-repositorio.git)
    cd tu-repositorio
    ```

2.  **Crear y activar un entorno virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3.  **Instalar dependencias:**
    *(Nota: Asumiendo que tienes un archivo `requirements.txt`)*
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar variables de entorno:**
    Crea un archivo `.env` en la raíz del proyecto (puedes copiarlo desde `.env.example` si existe) y añade tus credenciales:
    ```.env
    DB_URL="postgresql://BiblioUser:root@localhost:5432/biblioteca"
    JWT_SECRET="56b288b91746e72d13b3cc630fb37fa707cbd491170a13f62c68dfba12950809"
    ```

5.  **Ejecutar la aplicación:**
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ```

6.  **Acceder a la documentación de la API:**
    Abre tu navegador y ve a [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) para ver la interfaz de Swagger UI.

### Ejecución con Docker

Si tienes Docker instalado, puedes construir y ejecutar la imagen:

1.  **Construir la imagen:**
    ```bash
    docker build -t biblioteca-api .
    ```

2.  **Ejecutar el contenedor:**
    *(Asegúrate de pasar las variables de entorno. Es mejor usar `docker-compose` para esto en un escenario real)*
    ```bash
    docker run -p 8000:8000 \
      -e DB_URL="tu-url-de-db" \
      -e JWT_SECRET="tu-secreto" \
      biblioteca-api
    ```