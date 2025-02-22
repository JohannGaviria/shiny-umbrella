# Shiny Umbrella

Desarrollo de una API REST que permite a los usuarios crear y participar en encuestas. Ofrece gestión de perfiles, visualización de resultados y notificaciones sobre la actividad de las encuestas, facilitando la recopilación de datos para la toma de decisiones.

## Tecnologías Utilizadas

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)![DRF](https://img.shields.io/badge/DRF-000000?style=for-the-badge&logo=django&logoColor=white)![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)![Shell](https://img.shields.io/badge/Shell-4EAA25?style=for-the-badge&logo=gnubash&logoColor=white)![TestsCase](https://img.shields.io/badge/TestsCase-000000?style=for-the-badge&logo=jest&logoColor=white)![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)[![REST API](https://img.shields.io/badge/REST_API-005571?style=for-the-badge&logo=api&logoColor=white)](https://restfulapi.net/)

## Tabla de Contenidos

- [Instalación](#instalación)
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

3. **Crea las variables de entorno:**
- Crea un archivo `.env` en la raíz del proyecto y configura las siguientes variables:
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

1. **Construir y ejecutar los contenedores:**

```bash
docker compose -f docker/docker-compose.dev.yml build
docker compose -f docker/docker-compose.dev.yml up
```

¡Listo! El proyecto ahora debería estar en funcionamiento en tu entorno con docker. Puedes acceder a él desde tu navegador web visitando `http://0.0.0.0:8000/`.

### Entorno Local

**Requisitos:**
- Python
- PostgreSQL

1. **Instalar las dependencias:**

```bash
pip install -r requirements.txt
```

2. **Crea las migraciones:**

```bash
python manage.py makemigrations --settings=config.settings.development
python manage.py migrate --settings=config.settings.development
```

3. **Ejecutar el servidor:**

```bash
python manage.py runserver --settings=config.settings.development
```

¡Listo! El proyecto ahora debería estar en funcionamiento en tu entorno local. Puedes acceder a él desde tu navegador web visitando `http://127.0.0.1:8000/`.

---

## Endpoints

### Usuarios

| Nombre | Método | URL | Descripción |
|:------ | :----- | :-- | :---------- |
| [Registro de usuarios](#registro-de-usuario) | `POST` | `/api/users/sign_up` | Registro de usuarios en el sistema. |
| [Verificación de correo electrónico del usuario](#verificación-del-correo-electrónico-del-usuario) | `GET` | `/api/users/verify/<str:token_email>` | Verificación del correo electrónico del usuario. |
| [Inicio de sesión de usuarios](#inicio-de-sesión-de-usuario) | `POST` | `/api/users/sign_in` | Inicio de sesión de los usuarios en el sistema. |
| [Cierre de sesión de usuarios](#cierre-de-sesión-de-usuario) | `POST` | `/api/users/sign_out` | Cierre de sesión de los usuarios en el sistema. |
| [Actualización de usuarios](#actualización-del-usuario) | `PUT` | `/api/users/update_user` | Actualizar la información del perfil del usuario. |
| [Eliminación de usuarios](#eliminación-del-usuario) | `DELETE` | `/api/users/delete_user` | Eliminar el usuario actual. |

#### Registro de usuario

##### Método HTTP

```http
POST /api/users/sign_up
```

##### Parámetros

| Parámetro | Tipo     | Descripción                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Requerido**. Nombre de usuario |
| `email` | `string` | **Requerido**. Correo electrónico del usuario |
| `password` | `string` | **Requerido**. Contraseña del usuario |

##### Ejemplo de solicitud

```http
Content-Type: application/json

{
    "username": "testUsername",
    "email": "test@email.com",
    "password": "testPassword"
}
```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 201 CREATED
Content-Type: application/json

{
    "status": "success",
    "message": "User registered successfully.",
    "data": {
        "token": {
            "token_key": "b14407b771de4372bb3fd864a7d4b12884b8db09"
        },
        "user": {
            "id": 1,
            "username": "testUsername",
            "email": "test@email.com",
            "date_joined": "2024-10-14T00:12:52.125524Z"
        }
    }
}
```

#### Verificación del correo electrónico del usuario

##### Método HTTP

```http
GET /api/users/verify/<str:token_email>
```

##### Parámetros

| Parámetro | Tipo     | Descripción                |
| :-------- | :------- | :------------------------- |
| `token_email` | `string` | **Requerido**. Token de verificación del correo electrónico |

> **NOTA**: El `token_email` se obtiene en la bandeja de entrada del correo electrónico proporcionado al registrarse.

##### Ejemplo de solicitud

```http
Content-Type: application/json  
```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "status": "success",
    "message": "Email verified successfully."
}
```

#### Inicio de sesión de usuario

##### Método HTTP

```http
POST /api/users/sign_in
```

##### Parámetros

| Parámetro | Tipo     | Descripción                |
| :-------- | :------- | :------------------------- |
| `email` | `string` | **Requerido**. Correo electrónico del usuario |
| `password` | `string` | **Requerido**. Contraseña del usuario |

##### Ejemplo de solicitud

```http
Content-Type: application/json

{
    "email": "test@email.com",
    "password": "testPassword"
}
```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "status": "success",
    "message": "User logged in successfully.",
    "data": {
        "token": {
            "token_key": "b14407b771de4372bb3fd864a7d4b12884b8db09",
            "token_expiration": "2024-10-17T23:50:09.865811+00:00"
        },
        "user": {
            "id": 1,
            "username": "testUsername",
            "email": "test@email.com",
            "date_joined": "2024-10-14T00:12:52.125524Z"
        }
    }
}
```

#### Cierre de sesión de usuario

##### Método HTTP

```http
POST /api/users/sign_out
```

##### Parámetros

| Parámetro | Tipo     | Descripción                |
| :-------- | :------- | :------------------------- |
| `Token` | `string` | **Requerido**. Token de autenticación |

##### Ejemplo de solicitud

```http
Content-Type: application/json
Authorization: Token <Token>
```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "status": "success",
    "message": "User logged out successfully."
}
```

#### Actualización del usuario

##### Método HTTP

```http
PUT /api/users/update_user
```

##### Parámetros

| Parámetro | Tipo     | Descripción                |
| :-------- | :------- | :------------------------- |
| `Token` | `string` | **Requerido**. Token de autenticación |
| `username` | `string` | **Requerido**. Nombre de usuario |
| `email` | `string` | **Requerido**. Correo electrónico del usuario |
| `current_password` | `string` | Contraseña actual del usuario |
| `new_password` | `string`	| Nueva contraseña del usuario |

##### Ejemplo de solicitud

```http
Content-Type: application/json
Authorization: Token <Token>

{
    "username": "TestNewUsername",
    "email": "testnew@email.com",
    "current_password": "TestPassword",
    "new_password": "TestNewPassword"
}
```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "status": "success",
    "message": "User profile updated successfully.",
    "data": {
        "token": {
            "token_key": "42b1c149a8e85094bd47123746fef49b8b1a6b6a",
            "token_expiration": "2024-10-23T23:52:42.931684+00:00"
        },
        "user": {
            "id": 1,
            "username": "TestNewUsername",
            "email": "testnew@email.com",
            "date_joined": "2024-10-20T23:16:47.695682Z"
        }
    }
}
```

#### Eliminación del usuario

##### Método HTTP

```http
DELETE /api/users/delete_user
```

##### Parámetros

| Parámetro | Tipo     | Descripción                |
| :-------- | :------- | :------------------------- |
| `Token` | `string` | **Requerido**. Token de autenticación |

##### Ejemplo de solicitud

```http
Content-Type: application/json
Authorization: Token <Token>
```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "status": "success",
    "message": "User deleted successfully."
}
```

---

### Encuestas

| Nombre | Método | Url | Descripción |
|:------ | :----- | :-- | :---------- |
| [Crear encuesta](#crear-encuesta) | `POST` | `/api/surveys/create` | Crea una nueva encuesta. |
| [Obtener una encuesta por ID](#obtener-encuesta-por-id) | `GET` | `/api/surveys/get/<str:survey_id>` | Obtiene una encuesta mediante su ID. |
| [Obtener todas las encuestas](#obtener-todas-las-encuesta) | `GET` | `/api/surveys/get_all?page_size=<size_value>&page=<page_value>` | Obtiene todas las encuestas. |
| [Buscar encuestas](#buscar-encuestas) | `GET` | `/api/surveys/search_surveys?query=<search_value>&page_size=<size_value>&page=<page_value>` | Busca las encuestas. |
| [Actualizar una encuesta](#actualizar-una-encuesta) | `PUT` | `/api/surveys/update/<str:survey_id>` | Actualiza una encuesta por su ID. |
| [Eliminar una encuesta](#eliminar-una-encuesta) | `DELETE` | `/api/surveys/delete/<str:survey_id>` | Elimina una encuesta por su ID. |
| [Responder una encuesta](#responder-una-encuesta) | `POST` | `/api/surveys/<str:survey_id>/answer` | Responde a una encuesta. |
| [Invitar a Responder una encuesta](#invitar-a-responder-una-encuesta) | `POST` | `/api/surveys/<str:survey_id>/invite` | Invita a responde a una encuesta. |

#### Crear encuesta

##### Método HTTP

```http
POST /api/surveys/create
```

##### Parámetros

| Parámetro | Tipo     | Descripción                |
| :-------- | :------- | :------------------------- |
| `Token` | `string` | **Requerido**.  Token de autenticación |
| `title` | `string` | **Requerido**.  Titulo de la encuesta |
| `description` | `string` | Descripcion de la encuesta |
| `start_date` | `datetime` | Fecha de iniciación de la encuesta |
| `end_date` | `datetime` | **Requerido**.  Fecha de finalización de la encuesta |
| `is_public` | `bool` | Visibilidad de la encuesta |
| `asks` | `array` | Lista de preguntas asociadas a la encuesta |

> **NOTA**: El parámetro `start_date` es opcional; si no se proporciona, tomará por defecto la fecha actual.

> **NOTA**: El parámetro `is_public` acepta los siguientes valores:
>
> - **true**: Indica que la encuesta es pública.
> - **false**: Indica que la encuesta es privada.
> - **null**: El campo tomaria por defecto la propiedad `false`.

**Estructura de `asks`**

| Parámetro    | Tipo      | Descripción                                           |
| :----------- | :-------- | :--------------------------------------------------- |
| `text`       | `string`  | **Requerido**. Texto de la pregunta                  |
| `type`       | `string`  | **Requerido**. Tipo de pregunta |
| `options`    | `array`   | Lista de opciones de respuesta |

> **NOTA**: El parámetro `type` solo acepta los siguientes valores:
>
> - **multiple**: Indica que la pregunta es de opción multiple.
> - **short**: Indica que la pregunta es de respuesta corta.
> - **boolean**: Indica que la pregunta es de verdadero o falso.

> **NOTA**: El parámetro `options` solo es requerido para preguntas tipo `multiple`

**Estructura de `options`**

| Parámetro    | Tipo      | Descripción                                           |
| :----------- | :-------- | :--------------------------------------------------- |
| `text`       | `string`  | **Requerido**. Texto de la opción |


##### Ejemplo de solicitud

```http
Content-Type: application/json
Authorization: Token <Token>

{
    "title": "Title of the surveys",
    "description": "Description of the surveys.",
    "end_date": "2024-10-29 21:39:50.764361",
    "is_public": true,
    "asks": [
        {
            "text": "This is a multiple choice question",
            "type": "multiple",
            "options": [
                {"text": "Option 1"},
                {"text": "Option 2"},
                {"text": "Option 3"}
            ]
        },
        {
            "text": "This is a true or false question",
            "type": "boolean"
        },
        {
            "text": "This is a short answer question",
            "type": "short"
        }
    ]
}
```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 201 CREATED
Content-Type: application/json

{
    "status": "success",
    "message": "Survey created successfully.",
    "data": {
        "survey": {
            "id": "74b604fcd9044fbe9afddb735a05e07e",
            "title": "Title of the surveys",
            "description": "Description of the surveys.",
            "start_date": "2024-10-28T01:55:01.828617Z",
            "end_date": "2024-10-29T21:39:50.764361Z",
            "is_public": true,
            "user": {
                "id": 1,
                "username": "testUsername",
                "email": "test@email.com",
                "date_joined": "2024-10-14T00:12:52.125524Z"
            },
            "asks": [
                {
                    "text": "This is a multiple choice question",
                    "type": "multiple",
                    "options": [
                        {
                            "text": "Option 1"
                        },
                        {
                            "text": "Option 2"
                        },
                        {
                            "text": "Option 3"
                        }
                    ]
                },
                {
                    "text": "This is a true or false question",
                    "type": "boolean",
                    "options": []
                },
                {
                    "text": "This is a short answer question",
                    "type": "short",
                    "options": []
                }
            ]
        }
    }
}
```

#### Obtener encuesta por id

##### Método HTTP

```http
GET /api/surveys/get/<str:survey_id>
```

##### Parámetros

| Parámetro | Tipo     | Descripción                |
| :-------- | :------- | :------------------------- |
| `Token` | `string` | **Requerido**.  Token de autenticación |
| `survey_id` | `string` | **Requerido**.  ID de la encuesta |

##### Ejemplo de solicitud

```http
Content-Type: application/json
Authorization: Token <Token>
```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 200 Ok
Content-Type: application/json

{
    "status": "success",
    "message": "Survey successfully obtained.",
    "data": {
        "survey": {
            "id": "74b604fcd9044fbe9afddb735a05e07e",
            "title": "Title of the surveys",
            "description": "Description of the surveys.",
            "start_date": "2024-10-28T01:55:01.828617Z",
            "end_date": "2024-10-29T21:39:50.764361Z",
            "is_public": true,
            "user": {
                "id": 1,
                "username": "testUsername",
                "email": "test@email.com",
                "date_joined": "2024-10-14T00:12:52.125524Z"
            },
            "asks": [
                {
                    "text": "This is a multiple choice question",
                    "type": "multiple",
                    "options": [
                        {
                            "text": "Option 1"
                        },
                        {
                            "text": "Option 2"
                        },
                        {
                            "text": "Option 3"
                        }
                    ]
                },
                {
                    "text": "This is a true or false question",
                    "type": "boolean",
                    "options": []
                },
                {
                    "text": "This is a short answer question",
                    "type": "short",
                    "options": []
                }
            ]
        }
    }
}
```

#### Obtener todas las encuesta

##### Método HTTP

```http
GET /api/surveys/get_all?page_size=<size_value>&page=<page_value>
```

##### Parámetros

| Parámetro | Tipo     | Descripción                |
| :-------- | :------- | :------------------------- |
| `Token` | `string` | **Requerido**.  Token de autenticación |
| `size_value` | `int` | Valor del tamaño de elementos por página |
| `page_value` | `int` | Valor de la página para navegar entre la paginación |

> **NOTA**: Si los parámetros `page_size` y `page` no se incluyen en la URL, se aplicarán valores por defecto:
>
> - **Ejemplo**: `GET /api/surveys/get_all`
>   - **page_size** será `10`, lo que significa que se mostrarán 10 elementos por página.
>   - **page** será `1`, comenzando en la primera página de la paginación.
> - **Recomendación**: Para navegar entre las páginas, debe incluir el parámetro page e indicar el número de la página a la que desea acceder.

##### Ejemplo de solicitud

```http
Content-Type: application/json
Authorization: Token <Token>
```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 200 Ok
Content-Type: application/json

{
    "status": "success",
    "message": "Surveys successfully obtained.",
    "data": {
        "page_info": {
            "count": 21,
            "page_size": 5,
            "links": {
                "next": "http://127.0.0.1:8000/api/surveys/get_all?page=2&page_size=5,
                "previous": null
            }
        },
        "surveys": [
            {
                "id": "74b604fcd9044fbe9afddb735a05e07e",
                "title": "Title of the surveys",
                "description": "Description of the surveys.",
                "start_date": "2024-10-28T01:55:01.828617Z",
                "end_date": "2024-10-29T21:39:50.764361Z",
                "is_public": true,
                "user": {
                    "id": 1,
                    "username": "testUsername",
                    "email": "test@email.com",
                    "date_joined": "2024-10-14T00:12:52.125524Z"
                },
                "asks": [
                    {
                        "text": "This is a multiple choice question",
                        "type": "multiple",
                        "options": [
                            {
                                "text": "Option 1"
                            },
                            {
                                "text": "Option 2"
                            },
                            {
                                "text": "Option 3"
                            }
                        ]
                    },
                    {
                        "text": "This is a true or false question",
                        "type": "boolean",
                        "options": []
                    },
                    {
                        "text": "This is a short answer question",
                        "type": "short",
                        "options": []
                    }
                ]
            }
        ]
    }
}
```

#### Buscar encuestas

##### Método HTTP

```http
GET /api/surveys/search_surveys?query=<search_value>&page_size=<size_value>&page=<page_value>
```

##### Parámetros

| Parámetro | Tipo     | Descripción                |
| :-------- | :------- | :------------------------- |
| `Token` | `string` | **Requerido**.  Token de autenticación |
| `search_value` | `string` | Valor del párametro de búsqueda |
| `size_value` | `int` | Valor del tamaño de elementos por página |
| `page_value` | `int` | Valor de la página para navegar entre la paginación |

> **NOTA**: El parámetro `search_value` Busca encuestas por:
>
> - **title**: Titulo de la encuesta.
> - **description**: Descripcion de la encuesta.
> - **user**: Usuario creador de la encuesta.

> **NOTA**: Si los parámetros `page_size` y `page` no se incluyen en la URL, se aplicarán valores por defecto:
>
> - **Ejemplo**: `GET /api/surveys/search_surveys?query=<search_value>`
>   - **page_size** será `10`, lo que significa que se mostrarán 10 elementos por página.
>   - **page** será `1`, comenzando en la primera página de la paginación.
> - **Recomendación**: Para navegar entre las páginas, debe incluir el parámetro page e indicar el número de la página a la que desea acceder.

##### Ejemplo de solicitud

```http
Content-Type: application/json
Authorization: Token <Token>
```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 200 Ok
Content-Type: application/json

{
    "status": "success",
    "message": "Searching for surveys successfully.",
    "data": {
        "page_info": {
            "count": 21,
            "page_size": 5,
            "links": {
                "next": "http://127.0.0.1:8000/api/surveys/search_survey?page=2&page_size=5&query="Title of the",
                "previous": null
            }
        },
        "surveys": [
            {
                "id": "74b604fcd9044fbe9afddb735a05e07e",
                "title": "Title of the surveys",
                "description": "Description of the surveys.",
                "start_date": "2024-10-28T01:55:01.828617Z",
                "end_date": "2024-10-29T21:39:50.764361Z",
                "is_public": true,
                "user": {
                    "id": 1,
                    "username": "testUsername",
                    "email": "test@email.com",
                    "date_joined": "2024-10-14T00:12:52.125524Z"
                },
                "asks": [
                    {
                        "text": "This is a multiple choice question",
                        "type": "multiple",
                        "options": [
                            {
                                "text": "Option 1"
                            },
                            {
                                "text": "Option 2"
                            },
                            {
                                "text": "Option 3"
                            }
                        ]
                    },
                    {
                        "text": "This is a true or false question",
                        "type": "boolean",
                        "options": []
                    },
                    {
                        "text": "This is a short answer question",
                        "type": "short",
                        "options": []
                    }
                ]
            },
            ...
        ]
    }
}
```

#### Actualizar una encuesta

##### Método HTTP

```http
PUT /api/surveys/update/<str:survey_id>
```

##### Parámetros

| Parámetro | Tipo     | Descripción                |
| :-------- | :------- | :------------------------- |
| `Token` | `string` | **Requerido**.  Token de autenticación |
| `title` | `string` | Titulo de la encuesta |
| `description` | `string` | Descripcion de la encuesta |
| `start_date` | `datetime` | Fecha de iniciación de la encuesta |
| `end_date` | `datetime` | Fecha de finalización de la encuesta |
| `is_public` | `bool` | Visibilidad de la encuesta |
| `asks` | `array` | Lista de preguntas asociadas a la encuesta |

> **NOTA**: El parámetro `start_date` es opcional; si no se proporciona, tomará por defecto la fecha actual.

> **NOTA**: El parámetro `is_public` acepta los siguientes valores:
>
> - **true**: Indica que la encuesta es pública.
> - **false**: Indica que la encuesta es privada.
> - **null**: El campo tomaria por defecto la propiedad `false`.

**Estructura de `asks`**

| Parámetro    | Tipo      | Descripción                                           |
| :----------- | :-------- | :--------------------------------------------------- |
| `text`       | `string`  | Texto de la pregunta                  |
| `type`       | `string`  | Tipo de pregunta |
| `options`    | `array`   | Lista de opciones de respuesta |

> **NOTA**: El parámetro `type` solo acepta los siguientes valores:
>
> - **multiple**: Indica que la pregunta es de opción multiple.
> - **short**: Indica que la pregunta es de respuesta corta.
> - **boolean**: Indica que la pregunta es de verdadero o falso.

> **NOTA**: El parámetro `options` solo es requerido para preguntas tipo `multiple`

**Estructura de `options`**

| Parámetro    | Tipo      | Descripción                                           |
| :----------- | :-------- | :--------------------------------------------------- |
| `text`       | `string`  | Texto de la opción |

##### Ejemplo de solicitud

```http
Content-Type: application/json
Authorization: Token <Token>

{
    "title": "Title of the surveys",
    "description": "Description of the surveys.",
    "end_date": "2024-10-29 21:39:50.764361",
    "is_public": true,
    "asks": [
        {
            "text": "This is a multiple choice question",
            "type": "multiple",
            "options": [
                {"text": "Option 1"},
                {"text": "Option 2"},
                {"text": "Option 3"}
            ]
        },
        {
            "text": "This is a true or false question",
            "type": "boolean"
        },
        {
            "text": "This is a short answer question",
            "type": "short"
        }
    ]
}
```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 200 Ok
Content-Type: application/json

{
    "status": "success",
    "message": "Survey update successfully.",
    "data": {
        "survey": {
            "id": "74b604fcd9044fbe9afddb735a05e07e",
            "title": "Title of the surveys",
            "description": "Description of the surveys.",
            "start_date": "2024-10-28T01:55:01.828617Z",
            "end_date": "2024-10-29T21:39:50.764361Z",
            "is_public": true,
            "user": {
                "id": 1,
                "username": "testUsername",
                "email": "test@email.com",
                "date_joined": "2024-10-14T00:12:52.125524Z"
            },
            "asks": [
                {
                    "text": "This is a multiple choice question",
                    "type": "multiple",
                    "options": [
                        {
                            "text": "Option 1"
                        },
                        {
                            "text": "Option 2"
                        },
                        {
                            "text": "Option 3"
                        }
                    ]
                },
                {
                    "text": "This is a true or false question",
                    "type": "boolean",
                    "options": []
                },
                {
                    "text": "This is a short answer question",
                    "type": "short",
                    "options": []
                }
            ]
        }
    }
}
```

#### Eliminar una encuesta

##### Método HTTP

```http
DELETE /api/surveys/delete/<str:survey_id>
```

##### Parámetros

| Parámetro | Tipo     | Descripción                |
| :-------- | :------- | :------------------------- |
| `Token` | `string` | **Requerido**.  Token de autenticación |
| `survey_id` | `string` | **Requerido**.  ID de la encuesta |

##### Ejemplo de solicitud

```http
Content-Type: application/json
Authorization: Token <Token>
```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 200 Ok
Content-Type: application/json

{
  "status": "success",
  "message": "Survey successfully deleted."
}
```

#### Responder una encuesta

##### Método HTTP

```http
POST /api/surveys/<str:survey_id>/answer
```

##### Parámetros

| Parámetro | Tipo     | Descripción                |
| :-------- | :------- | :------------------------- |
| `Token` | `string` | **Requerido**.  Token de autenticación |
| `answers` | `dict` | **Requerido**. Diccionario con las respuesta de la encuesta  |

**Estructura de `answers`**

| Parámetro    | Tipo      | Descripción                                           |
| :----------- | :-------- | :--------------------------------------------------- |
| `content_answer`       | `string`  | **Requerido**. Contenido de la respuesta |
| `ask`       | `string`  | **Requerido**. ID de la pregunta |
| `option`       | `string`  | **Requerido**. ID de la opción |

> **NOTA**: El parámetro `option` solo es requerido para respuesta a preguntas de tipo `multiple`

##### Ejemplo de solicitud

```http
Content-Type: application/json
Authorization: Token <Token>

{
    "answers": [
        {
            "content_answer": "Python",
            "ask": "c6d8b863-e67f-402a-b9c6-5ef2a7722a9e",
            "option": "e5474d9f-e4da-41cc-96a7-e1ea599fb613"
        },
        {
            "content_answer": "Backend",
            "ask": "eda4700e-5de8-4bb9-90a6-7b39bbc8ccfa"
        },
        {
            "content_answer": "True",
            "ask": "8a5d7fd1-7958-4b77-b2d5-60fbd3e90ad1"
        }
    ]
}

```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 201 CREATED
Content-Type: application/json

{
  "status": "success",
  "message": "Survey successfully answered.",
  "data": {
    "answers": [
      {
        "id": "267cd299-011e-49cd-8929-f54ec2288498",
        "user": {
          "id": 11,
          "username": "kalahad",
          "email": "kalahad631@chainds.com",
          "date_joined": "2024-10-13T23:16:20.500855Z"
        },
        "ask": {
          "id": "c6d8b863-e67f-402a-b9c6-5ef2a7722a9e",
          "text": "¿Cuál es tu lenguaje de programación favorito?",
          "type": "multiple",
          "options": [
            {
              "id": "e5474d9f-e4da-41cc-96a7-e1ea599fb613",
              "text": "Python"
            },
            {
              "id": "a8477c81-0699-46bf-adbc-3989a1bbcdc7",
              "text": "Java"
            },
            {
              "id": "3181a34f-d293-4c31-bba0-27529d80a45f",
              "text": "C++"
            },
            {
              "id": "0d4d84db-3b37-491f-b9e0-4f877ce4c353",
              "text": "C#"
            }
          ]
        },
        "content_answer": "Python",
        "option": {
          "id": "e5474d9f-e4da-41cc-96a7-e1ea599fb613",
          "text": "Python"
        }
      },
      {
        "id": "9a708c3f-0f17-40d7-ac46-0eac8e64bfbd",
        "user": {
          "id": 11,
          "username": "kalahad",
          "email": "kalahad631@chainds.com",
          "date_joined": "2024-10-13T23:16:20.500855Z"
        },
        "ask": {
          "id": "eda4700e-5de8-4bb9-90a6-7b39bbc8ccfa",
          "text": "¿Prefieres el desarrollo frontend o backend?",
          "type": "short",
          "options": []
        },
        "content_answer": "Backend",
        "option": null
      },
      {
        "id": "9bd8ab82-4988-4de9-acd3-1d2370162fe5",
        "user": {
          "id": 11,
          "username": "kalahad",
          "email": "kalahad631@chainds.com",
          "date_joined": "2024-10-13T23:16:20.500855Z"
        },
        "ask": {
          "id": "8a5d7fd1-7958-4b77-b2d5-60fbd3e90ad1",
          "text": "¿Crees que Python es fácil de aprender?",
          "type": "boolean",
          "options": []
        },
        "content_answer": "True",
        "option": null
      }
    ]
  }
}
```

#### Invitar a responder una encuesta

##### Método HTTP

```http
POST /api/surveys/<str:survey_id>/invite
```

##### Parámetros

| Parámetro | Tipo     | Descripción                |
| :-------- | :------- | :------------------------- |
| `Token` | `string` | **Requerido**.  Token de autenticación |
| `survey_id` | `string` | **Requerido**.  ID de la encuesta |
| `emails` | `array` | **Requerido**.  Lista con los correos electronicos |

##### Ejemplo de solicitud

```http
Content-Type: application/json
Authorization: Token <Token>

{
  "emails": [
    "invitee1@example.com",
    "invitee2@example.com",
    "invitee3@example.com"
  ]
}
```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 200 Ok
Content-Type: application/json

{
    'status': 'success',
    'message': 'Invitations sent successfully.'
}
```

### Feedback

| Nombre | Método | Url | Descripción |
|:------ | :----- | :-- | :---------- |
| [Agregar comentario](#agregar-comentario) | `POST` | `/api/feedbacks/survey/<str:survey_id>/comment/add` | Agregar un comentario a una encuesta. |
| [Obtener todos los comentarios de una encuesta](#obtener-todos-los-comentarios-de-una-encuesta) | `GET` | `/api/feedbacks/survey/<str:survey_id>/comment/all?page_size=<size_value>&page=<page_value>` | Obtiene todos los comentarios de una encuesta. |
| [Actualizar un comentario](#actualizar-un-comentario) | `PUT` | `/api/feedbacks/survey/<str:survey_id>/comment/<int:comment_id>/update` | Actualiza un comentario de una encuesta. |
| [Eliminar un comentario](#eliminar-un-comentario) | `DELETE` | `/api/feedbacks/survey/<str:survey_id>/comment/<int:comment_id>/delete` | Elimina un comentario de una encuesta. |
| [Agregar calificación](#agregar-calificación) | `POST` | `/api/feedbacks/survey/<str:survey_id>/qualify/add` | Agregar una calificación a una encuesta. |
| [Obtener todos las calificaciones de una encuesta](#obtener-todos-las-calificaciones-de-una-encuesta) | `GET` | `/api/feedbacks/survey/<str:survey_id>/qualify/all?page_size=<size_value>&page=<page_value>` | Obtiene todas las calificaciones de una encuesta. |
| [Actualizar una calificación](#actualizar-una-calificación) | `PUT` | `/api/feedbacks/survey/<str:survey_id>/qualify/<int:qualify_id>/update` | Actualiza una calificación de una encuesta. |
| [Eliminar una calificación](#eliminar-una-calificación) | `DELETE` | `/api/feedbacks/survey/<str:survey_id>/qualify/<int:qualify_id>/delete` | Elimina una calificación de una encuesta. |

#### Agregar comentario

##### Método HTTP

```http
POST /api/feedbacks/survey/<str:survey_id>/comment/add
```

##### Parámetros

| Parámetro | Tipo     | Descripción                |
| :-------- | :------- | :------------------------- |
| `Token` | `string` | **Requerido**.  Token de autenticación |
| `content` | `string` | **Requerido**.  Contenido del comentario |

##### Ejemplo de solicitud

```http
Content-Type: application/json
Authorization: Token <Token>

{
    "content": "The survey was interesting, but I wish it included more open-ended questions so I could express my opinion better."
}
```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 201 CREATED
Content-Type: application/json

{
  "status": "success",
  "message": "Comment added successfully."
}
```

#### Obtener todos los comentarios de una encuesta

##### Método HTTP

```http
GET /api/feedbacks/survey/<str:survey_id>/comment/all?page_size=<size_value>&page=<page_value>
```

##### Parámetros

| Parámetro | Tipo     | Descripción                |
| :-------- | :------- | :------------------------- |
| `Token` | `string` | **Requerido**.  Token de autenticación |
| `survey_id` | `string` | **Requerido**.  ID de la encuesta |
| `size_value` | `int` | Valor del tamaño de elementos por página |
| `page_value` | `int` | Valor de la página para navegar entre la paginación |

> **NOTA**: Si los parámetros `page_size` y `page` no se incluyen en la URL, se aplicarán valores por defecto:
>
> - **Ejemplo**: `GET /api/feedbacks/survey/<str:survey_id>/comment/all`
>   - **page_size** será `10`, lo que significa que se mostrarán 10 elementos por página.
>   - **page** será `1`, comenzando en la primera página de la paginación.
> - **Recomendación**: Para navegar entre las páginas, debe incluir el parámetro page e indicar el número de la página a la que desea acceder.

##### Ejemplo de solicitud

```http
Content-Type: application/json
Authorization: Token <Token>
```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "status": "success",
  "message": "Comments successfully obtained.",
  "data": {
    "page_info": {
      "count": 1,
      "page_size": 10,
      "links": {
        "next": null,
        "previous": null
      }
    },
    "comments": [
      {
        "id": 1,
        "content": "The survey was interesting, but I wish it included more open-ended questions so I could express my opinion better.",
        "created_at": "2024-11-30T22:02:20.045014Z",
        "survey": "74b604fcd9044fbe9afddb735a05e07e",
        "user": {
            "id": 2,
            "username": "testUsername2",
            "email": "test2@email.com",
            "date_joined": "2024-10-14T00:12:52.125524Z"
        }
      }
    ]
  }
}
```

#### Actualizar un comentario

##### Método HTTP

```http
PUT /api/feedbacks/survey/<str:survey_id>/comment/<int:comment_id>/update
```

##### Parámetros

| Parámetro | Tipo     | Descripción                |
| :-------- | :------- | :------------------------- |
| `Token` | `string` | **Requerido**.  Token de autenticación |
| `survey_id` | `str` | **Requerido**.  ID de la encuesta |
| `comment_id` | `int` | **Requerido**.  ID del comentario |
| `content` | `string` | Contenido del comentario |

##### Ejemplo de solicitud

```http
Content-Type: application/json
Authorization: Token <token>

{
    "content": "The survey was interesting."
}
```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 200 Ok
Content-Type: application/json

{
  "status": "success",
  "message": "Comment updated successfully."
}
```

#### Eliminar un comentario

##### Método HTTP

```http
DELETE /api/feedbacks/survey/<str:survey_id>/comment/<int:comment_id>/delete
```

##### Parámetros

| Parámetro | Tipo     | Descripción                |
| :-------- | :------- | :------------------------- |
| `Token` | `string` | **Requerido**.  Token de autenticación |
| `survey_id` | `str` | **Requerido**.  ID de la encuesta |
| `comment_id` | `int` | **Requerido**.  ID del comentario |

##### Ejemplo de solicitud

```http
Content-Type: application/json
Authorization: Token <Token>
```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 200 Ok
Content-Type: application/json

{
  "status": "success",
  "message": "Comment successfully deleted."
}
```

#### Agregar calificación

##### Método HTTP

```http
POST /api/feedbacks/survey/<str:survey_id>/qualify/add
```

##### Parámetros

| Parámetro | Tipo     | Descripción                |
| :-------- | :------- | :------------------------- |
| `Token` | `string` | **Requerido**.  Token de autenticación |
| `assessment` | `int` | **Requerido**.  Número de la calificación |

> **NOTA**: El parámetro `assessment` solo acepta una escalara de valores de 1 a 5:

##### Ejemplo de solicitud

```http
Content-Type: application/json
Authorization: Token <Token>

{
    "assessment": 3
}
```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 201 CREATED
Content-Type: application/json

{
  "status": "success",
  "message": "Comment added successfully."
}
```

#### Obtener todos las calificaciones de una encuesta

##### Método HTTP

```http
GET /api/feedbacks/survey/<str:survey_id>/qualify/all?page_size=<size_value>&page=<page_value>
```

##### Parámetros

| Parámetro | Tipo     | Descripción                |
| :-------- | :------- | :------------------------- |
| `Token` | `string` | **Requerido**.  Token de autenticación |
| `survey_id` | `string` | **Requerido**.  ID de la encuesta |
| `size_value` | `int` | Valor del tamaño de elementos por página |
| `page_value` | `int` | Valor de la página para navegar entre la paginación |

> **NOTA**: Si los parámetros `page_size` y `page` no se incluyen en la URL, se aplicarán valores por defecto:
>
> - **Ejemplo**: `GET /api/feedbacks/survey/<str:survey_id>/qualify/all`
>   - **page_size** será `10`, lo que significa que se mostrarán 10 elementos por página.
>   - **page** será `1`, comenzando en la primera página de la paginación.
> - **Recomendación**: Para navegar entre las páginas, debe incluir el parámetro page e indicar el número de la página a la que desea acceder.

##### Ejemplo de solicitud

```http
Content-Type: application/json
Authorization: Token <Token>
```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 200 Ok
Content-Type: application/json

{
  "status": "success",
  "message": "Qualifies successfully obtained.",
  "data": {
    "page_info": {
      "count": 1,
      "page_size": 10,
      "links": {
        "next": null,
        "previous": null
      }
    },
    "qualifies": [
      {
        "id": 1,
        "assessment": 5,
        "survey": "74b604fcd9044fbe9afddb735a05e07e",
        "user": {
            "id": 2,
            "username": "testUsername2",
            "email": "test2@email.com",
            "date_joined": "2024-10-14T00:12:52.125524Z"
        }
      }
    ]
  }
}
```

#### Actualizar una calificación

##### Método HTTP

```http
PUT /api/feedbacks/survey/<str:survey_id>/qualify/<int:qualify_id>/update
```

##### Parámetros

| Parámetro | Tipo     | Descripción                |
| :-------- | :------- | :------------------------- |
| `Token` | `string` | **Requerido**.  Token de autenticación |
| `survey_id` | `str` | **Requerido**.  ID de la encuesta |
| `qualify_id` | `int` | **Requerido**.  ID del comentario |
| `assessmnet` | `int` | Número de la califiación |

> **NOTA**: El parámetro `assessment` solo acepta una escalara de valores de 1 a 5:

##### Ejemplo de solicitud

```http
Content-Type: application/json
Authorization: Token <Token>

{
    "assessment": 4
}
```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 200 Ok
Content-Type: application/json

{
  "status": "success",
  "message": "Qualify updated successfully."
}
```

#### Eliminar una calificación

##### Método HTTP

```http
DELETE /api/feedbacks/survey/<str:survey_id>/qualify/<int:qualify_id>/delete
```

##### Parámetros

| Parámetro | Tipo     | Descripción                |
| :-------- | :------- | :------------------------- |
| `Token` | `string` | **Requerido**.  Token de autenticación |
| `survey_id` | `str` | **Requerido**.  ID de la encuesta |
| `qualify_id` | `int` | **Requerido**.  ID de la calificación |

##### Ejemplo de solicitud

```http
Content-Type: application/json
Authorization: Token <Token>
```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 200 Ok
Content-Type: application/json

{
  "status": "success",
  "message": "Qualify successfully deleted."
}
```

---

### Análisis

| Nombre | Método | Url | Descripción |
|:------ | :----- | :-- | :---------- |
| [Exportar detalles del analisis](#exportar-detalles-del-analisis) | `GET` | `/api/analysis/survey/<str:survey_id>/export` | Exporta los detalles del analisis de la encuestas |

#### Exportar detalles del analisis

##### Método HTTP

```http
GET /api/analysis/survey/<str:survey_id>/export
```

##### Parámetros

| Parámetro | Tipo     | Descripción                |
| :-------- | :------- | :------------------------- |
| `Token` | `string` | **Requerido**.  Token de autenticación |
| `survey_id` | `string` | **Requerido**.  ID de la encuesta |

##### Ejemplo de solicitud

```http
Content-Type: application/json
Authorization: Token <Token>
```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 200 Ok
Content-Type: application/json

{
    "status": "success",
    "message': "Export of the analysis successfully."
}
```
