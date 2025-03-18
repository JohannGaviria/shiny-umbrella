# Shiny Umbrella

API REST para la creación y gestión de encuestas, permitiendo a los usuarios participar, visualizar resultados y recibir notificaciones sobre la actividad de las encuestas. Esta herramienta facilita la recopilación de datos para una toma de decisiones informada.

## Tecnologías Utilizadas

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)![DRF](https://img.shields.io/badge/DRF-000000?style=for-the-badge&logo=django&logoColor=white)![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)![Shell](https://img.shields.io/badge/Shell-4EAA25?style=for-the-badge&logo=gnubash&logoColor=white)![TestsCase](https://img.shields.io/badge/TestsCase-000000?style=for-the-badge&logo=jest&logoColor=white)![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)![REST API](https://img.shields.io/badge/REST_API-005571?style=for-the-badge&logo=api&logoColor=white)![Railway](https://img.shields.io/badge/Deploy%20on%20Railway-0B0D0E?style=for-the-badge&logo=railway&logoColor=white)

## Tabla de Contenidos

- [Instalación](#instalación)
    - [Entorno con Docker](#entorno-con-docker)
    - [Entorno Local](#entorno-local)
- [Deploy](#deploy)
- [Endpoints](#endpoints)
    - [Usuarios](#usuarios)
    - [Encuestas](#encuestas)
    - [Feedback](#feedback)
    - [Análisis](#análisis)

## Instalación

### Pasos de Instalación

1. **Clona este repositorio:**

    ```bash
    git clone https://github.com/JohannGaviria/shiny-umbrella.git
    cd shiny-umbrella
    ```

2. **Crea el entorno virtual:**

    Utiliza `venv` o cualquier otro gestor de entornos virtuales. Luego, crea y activa el entorno virtual:

    ```bash
    python -m venv venv
    # En Windows
    venv\Scripts\activate
    # En Mac/Linux
    source venv/bin/activate
    ```

3. **Configurar las variables de entorno:**
    
    Crea un archivo `.env` en la raíz del proyecto y configura las siguientes variables:
    
    - `SECRET_KEY` -> Clave secreta para la configuración de Django.
    - `DB_NAME` -> Nombre de la base de datos.
    - `DB_USER` -> Usuario de la base de datos.
    - `DB_PASSWORD` -> Contraseña del usuario de la base de datos.
    - `DB_HOST` -> Host de la base de datos.
    - `DB_PORT` -> Puerto de la base de datos.
    - `DJANGO_SETTINGS_MODULE` -> Módulo de configuración de Django.
    - `EMAIL` -> Correo electrónico para el envío de notificaciones por email.
    - `PASSWORD` -> Contraseña del correo electrónico.
    - `SECURITY_PASSWORD_SALT` -> Contraseña segura que permitirá al módulo `itsdangerous` generar y verificar tokens de forma segura.
    - `FRONTEND_URL` -> URL de verificación que se enviará por correo electrónico.

### Entorno con Docker

**Requisitos:**
- Docker
- Docker Compose

1. **Actualizar las variables de entorno para la base de datos:**

    Actualiza las variables de entorno relacionadas con la base de datos creada con Docker:

    - `DB_NAME` -> Nombre de la base de datos.
    - `DB_USER` -> Usuario de la base de datos.
    - `DB_PASSWORD` -> Contraseña del usuario de la base de datos.
    - `DB_HOST` -> Host de la base de datos.
    - `DB_PORT` -> Puerto de la base de datos.

2. **Construir y ejecutar los contenedores:**

    ```bash
    docker compose -f docker/docker-compose.dev.yml up --build
    ```

¡Listo! El proyecto ahora debería estar en funcionamiento en tu entorno con Docker. Puedes acceder a él desde tu navegador web visitando `http://0.0.0.0:8000/`.

### Entorno Local

**Requisitos:**
- Python 3.x
- PostgreSQL

1. **Instalar las dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

2. **Actualizar las variables de entorno para la base de datos:**

    Actualiza las variables de entorno de la base de datos con los datos correspondientes de tu entorno local:

    - `DB_NAME` -> Nombre de la base de datos.
    - `DB_USER` -> Usuario de la base de datos.
    - `DB_PASSWORD` -> Contraseña del usuario de la base de datos.
    - `DB_HOST` -> Host de la base de datos.
    - `DB_PORT` -> Puerto de la base de datos.

3. **Crear las migraciones:**

    ```bash
    python manage.py makemigrations --settings=config.settings.development
    python manage.py migrate --settings=config.settings.development
    ```

4. **Ejecutar el servidor:**

    ```bash
    python manage.py runserver --settings=config.settings.development
    ```

¡Listo! El proyecto ahora debería estar en funcionamiento en tu entorno local. Puedes acceder a él desde tu navegador web visitando `http://127.0.0.1:8000/`.

---

## Deploy

El proyecto está desplegado en Railway, puedes acceder a la API en vivo aquí:

[![Deploy](https://img.shields.io/badge/Deploy%20on%20Railway-0B0D0E?style=for-the-badge&logo=railway&logoColor=white)](https://shiny-umbrella.johanngaviria.dev)

---

## Endpoints

### Usuarios

| Nombre | Método | URL | Descripción |
|:------ | :----- | :-- | :---------- |
| Registro de usuarios | `POST` | `/api/users/sign_up` | Permite a los usuarios registrarse en el sistema. |
| Verificación de correo electrónico del usuario | `GET` | `/api/users/verify/<str:token_email>` | Verifica el correo electrónico del usuario mediante un token. |
| Inicio de sesión de usuarios | `POST` | `/api/users/sign_in` | Permite a los usuarios iniciar sesión en el sistema. |
| Cierre de sesión de usuarios | `POST` | `/api/users/sign_out` | Permite a los usuarios cerrar sesión en el sistema. |
| Actualización de usuarios | `PUT` | `/api/users/update_user` | Actualiza la información del perfil del usuario. |
| Eliminación de usuarios | `DELETE` | `/api/users/delete_user` | Elimina la cuenta del usuario actual. |

---

### Encuestas

| Nombre | Método | URL | Descripción |
|:------ | :----- | :-- | :---------- |
| Crear encuesta | `POST` | `/api/surveys/create` | Crea una nueva encuesta en el sistema. |
| Obtener una encuesta por ID | `GET` | `/api/surveys/get/<str:survey_id>` | Obtiene los detalles de una encuesta específica mediante su ID. |
| Obtener todas las encuestas | `GET` | `/api/surveys/get_all?page_size=<size_value>&page=<page_value>` | Obtiene una lista de todas las encuestas con paginación. |
| Buscar encuestas | `GET` | `/api/surveys/search_surveys?query=<search_value>&page_size=<size_value>&page=<page_value>` | Busca encuestas basadas en un término de búsqueda. |
| Actualizar una encuesta | `PUT` | `/api/surveys/update/<str:survey_id>` | Actualiza los detalles de una encuesta específica mediante su ID. |
| Eliminar una encuesta | `DELETE` | `/api/surveys/delete/<str:survey_id>` | Elimina una encuesta específica mediante su ID. |
| Responder una encuesta | `POST` | `/api/surveys/<str:survey_id>/answer` | Envía respuestas a una encuesta específica. |
| Invitar a responder una encuesta | `POST` | `/api/surveys/<str:survey_id>/invite` | Invita a usuarios a responder una encuesta específica. |

---

### Feedback

| Nombre | Método | URL | Descripción |
|:------ | :----- | :-- | :---------- |
| Agregar comentario | `POST` | `/api/feedbacks/survey/<str:survey_id>/comment/add` | Agrega un comentario a una encuesta específica. |
| Obtener todos los comentarios de una encuesta | `GET` | `/api/feedbacks/survey/<str:survey_id>/comment/all?page_size=<size_value>&page=<page_value>` | Obtiene todos los comentarios de una encuesta específica con paginación. |
| Actualizar un comentario | `PUT` | `/api/feedbacks/survey/<str:survey_id>/comment/<int:comment_id>/update` | Actualiza un comentario específico de una encuesta. |
| Eliminar un comentario | `DELETE` | `/api/feedbacks/survey/<str:survey_id>/comment/<int:comment_id>/delete` | Elimina un comentario específico de una encuesta. |
| Agregar calificación | `POST` | `/api/feedbacks/survey/<str:survey_id>/qualify/add` | Agrega una calificación a una encuesta específica. |
| Obtener todas las calificaciones de una encuesta | `GET` | `/api/feedbacks/survey/<str:survey_id>/qualify/all?page_size=<size_value>&page=<page_value>` | Obtiene todas las calificaciones de una encuesta específica con paginación. |
| Actualizar una calificación | `PUT` | `/api/feedbacks/survey/<str:survey_id>/qualify/<int:qualify_id>/update` | Actualiza una calificación específica de una encuesta. |
| Eliminar una calificación | `DELETE` | `/api/feedbacks/survey/<str:survey_id>/qualify/<int:qualify_id>/delete` | Elimina una calificación específica de una encuesta. |

---

### Análisis

| Nombre | Método | URL | Descripción |
|:------ | :----- | :-- | :---------- |
| Exportar detalles del análisis | `GET` | `/api/analysis/survey/<str:survey_id>/export` | Exporta los detalles del análisis de una encuesta específica. |
