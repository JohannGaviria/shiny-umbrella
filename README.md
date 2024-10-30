# Python-Django-PostgreSQL-Encuestas

Desarrollo de una API REST que permite a los usuarios crear y participar en encuestas. Ofrece gestión de perfiles, visualización de resultados y notificaciones sobre la actividad de las encuestas, facilitando la recopilación de datos para la toma de decisiones.

![Diagrama](assets/diagrama.png)

## Tecnologías Utilizadas

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)![Railway](https://img.shields.io/badge/Railway-0B0D0E?style=for-the-badge&logo=railway&logoColor=white)


## Tabla de Contenidos

- [Instalación](#instalación)
- [Endpoints](#endpoints)
    - [Usuarios](#usuarios)
    - [Encuestas](#encuestas)


## Instalación

### Pasos de Instalación

1. **Clona este repositorio:**

```bash
git clone https://github.com/JohannGaviria/shiny-umbrella.git
```

2. **Crea el entorno virtual:**

Utiliza `virtualenv` o cualquier otro gestor de entornos virtuales. Si `virtualenv` no está instalado, puedes instalarlo con:

```bash
pip install virtualenv
```

Luego, crea y activa el entorno virtual:

```bash
python -m virtualenv venv
# En Windows
venv\Scripts\activate
# En Mac/Linux
source venv/bin/activate
```

3. **Crea las variables de entorno:**
- Crea un archivo `.env` en la ruta raiz del proyecto y configura las siguientes variables:
    - `EMAIL` -> Correo electronico para el envio de notificaciones por email.
    - `PASSWORD` -> La contraseña del correo electronico.
    - `SECURITY_PASSWORD_SALT` -> Contraseña segura para que el módulo itsdangerous pueda generar y verificar tokens de forma segura.
    - `FRONTEND_URL` -> Generar la URL de verificación que se enviará por correo electrónico.

3. **Instalar las dependencias:**

```bash
cd shiny-umbrella
pip install -r requirements.txt
```

4. **Crea las migraciones:**

```bash
python manage.py makemigrations --settings=config.settings.development
python manage.py migrate --settings=config.settings.development
```

5. **Ejecutar el servidor:**

```bash
python manage.py runserver --settings=config.settings.development
```

¡Listo! El proyecto ahora debería estar en funcionamiento en tu entorno local. Puedes acceder a él desde tu navegador web visitando `http://127.0.0.1:8000/`.

## Endpoints

### Usuarios

| Nombre | Método | Url | Descripción |
|:------ | :----- | :-- | :---------- |
| [Registro de Usuarios](#registro-de-usuario) | `POST` | `/api/users/sign_up` | Registro de usuarios en el sistema. |
| [Verificación de Correo Electronico de Usuarios](#verificación-del-correo-electronico-del-usuario) | `GET` | `/api/users/verify/<str:token_email>` | Verificación del correo electronico del usuario. |
| [Inicio de Sesión de Usuarios](#inicio-de-sesión-de-usuario) | `POST` | `/api/users/sign_in` | Inicio de sesión de los usuarios en el sistema. |
| [Cierre de Sesión de Usuarios](#cierre-de-sesión-de-usuario) | `POST` | `/api/users/sign_out` | Cierre de sesión de los usuarios en el sistema. |
| [Actualización de Usuarios](#actualización-del-usuario) | `PUT` | `/api/users/update_user` | Actualizar la información del perfil del usuario. |
| [Eliminación de Usuarios](#eliminación-del-usuario) | `DELETE` | `/api/users/delete_user` | Eliminar el usuario actual. |

#### Registro de usuario

##### Método HTTP

```http
POST /api/users/sign_up
```

##### Parámetros

| Parámetro | Tipo     | Descripción                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Requerido**. Nombre del usuario |
| `email` | `string` | **Requerido**.  Correo electrónico del usuario |
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
HTTP/1.1 201 Created
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

#### Verificación del correo electronico del usuario

##### Método HTTP

```http
GET /api/users/verify/<str:token_email>
```

##### Parámetros

| Parámetro | Tipo     | Descripción                |
| :-------- | :------- | :------------------------- |
| `token_email` | `string` | **Requerido**.  Token de email de verificación |

> **NOTA**: El `token_email` lo consigue en la bandeja de mensajes de su correo electronico agregado a la hora de registrarse

##### Ejemplo de solicitud

```http
Content-Type: application/json  
```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 200 Ok
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
| `email` | `string` | **Requerido**. Correo electronico del usuario |
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
HTTP/1.1 201 Created
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
Authorization: Token <token>
```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 200 Ok
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
| `username` | `string` | **Requerido**. Nombre del usuario |
| `email` | `string` | **Requerido**.  Correo electrónico del usuario |
| `current_password` | `string` | Contraseña actual del usuario |
| `new_password` | `string`	| Nueva contraseña del usuario |

##### Ejemplo de solicitud

```http
Content-Type: application/json
Authorization: Token <token>

{
    "username": "TestNewUsername",
    "email": "testnew@email.com",
    "current_password": "TestPassword",
    "new_password": "TestNewPassword"
}
```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 200 Ok
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
Authorization: Token <token>
```

##### Ejemplo de respuesta exitosa

```http
HTTP/1.1 200 Ok
Content-Type: application/json

{
    "status": "success",
    "message": "User deleted successfully."
}
```

### Encuestas

| Nombre | Método | Url | Descripción |
|:------ | :----- | :-- | :---------- |
| [Crear cuenta](#crear-encuesta) | `POST` | `/api/surveys/create` | Crea una nueva encuesta. |
| [Obtener una cuenta por ID](#obtener-encuesta-por-id) | `GET` | `/api/surveys/get/<str:survey_id>` | Obtiene una encuesta mediante su ID. |

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
Authorization: Token <token>

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
    "message": "Survey created successfully.",
    "data": {
        "survey": {
            "title": "Title of the surveys",
            "description": "Description of the surveys.",
            "start_date": "2024-10-28T01:55:01.828617Z",
            "end_date": "2024-10-29T21:39:50.764361Z",
            "is_public": true,
            "user": {
                "id": 29,
                "username": "ropage",
                "email": "ropage7279@bulatox.com",
                "date_joined": "2024-10-28T01:10:20.683512Z"
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

#### 

##### Método HTTP

```http
GET /api/surveys/get/<str:survey_id>
```

##### Parámetros

| Parámetro | Tipo     | Descripción                |
| :-------- | :------- | :------------------------- |
| `token` | `string` | **Requerido**.  Token de autenticación |
| `survey_id` | `string` | **Requerido**.  ID de la encuesta |

##### Ejemplo de solicitud

```http
Content-Type: application/json
Authorization: Token <token>
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
            "title": "Title of the surveys",
            "description": "Description of the surveys.",
            "start_date": "2024-10-28T01:55:01.828617Z",
            "end_date": "2024-10-29T21:39:50.764361Z",
            "is_public": true,
            "user": {
                "id": 29,
                "username": "ropage",
                "email": "ropage7279@bulatox.com",
                "date_joined": "2024-10-28T01:10:20.683512Z"
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
