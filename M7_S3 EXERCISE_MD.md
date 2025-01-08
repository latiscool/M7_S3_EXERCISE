M7_S3 EXERCISE


## 1.- Crear entorno virtual en Python para trabajar con Django.
```	
pip install virtualenvwrapper
mkvirtualenv django-orm-postgresql
workon django-orm-postgresql # (para ingresar al entorno, en caso de NO ingresar automaticamente)
```	

## 2: Creación de la base de datos y usuario en PostgreSQL
#### #En la consola de SQL shell
```	
psql
Server [localhost]: ENTER
Database [postgres]:ENTER
Port [5432]:ENTER
Username [postgres]:ENTER
Contraseña para usuario postgres: postgresql
```	
```	
CREATE DATABASE project_orm_django ;
```	
#### #Cambio de BD
	\c project_orm_django;
	CREATE USER userdjango  WITH PASSWORD 'userdjango ';
	ALTER ROLE userdjango  SET default_transaction_isolation TO 'read committed';
	ALTER ROLE userdjango  SET timezone TO 'UTC';
	GRANT ALL PRIVILEGES ON SCHEMA public TO userdjango;
	ALTER ROLE userdjango SET search_path TO public;
	```	


## Etapa 3: Creación del proyecto Django

```
mkdir django-orm-postgresql  #mkdir Nombre_del_Proyecto
cd django-orm-postgresql
django-admin startproject config .

pip install django
pip install psycopg2  # El driver psycopg2 es necesario para que Django pueda comunicarse con PostgreSQL.
```

#### #En config/settings.py
```	
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'project_orm_django',  # Nombre de tu base de datos
        'USER': 'userdjango',          # Usuario creado en PostgreSQL
        'PASSWORD': 'userdjango',      # Contraseña del usuario
        'HOST': 'localhost',           # Dirección del servidor de la base de datos
        'PORT': '',                    # Puerto (vacío usa el predeterminado: 5432)
    }
}
```	
#### #En CMD verificar que Django puede conectarse a PostgreSQL:
```	
python manage.py check System check identified no issues (0 silenced). #Significa esta ok la conexion
```	


## Etapa 4: Migración de la base de datos y probando el proyecto

#### #En CMD del Proyecto
```	
python manage.py makemigrations   #: Escanea los modelos del proyecto y genera archivos de migración.
python manage.py migrate    #: Aplica los cambios descritos en las migraciones a la base de datos.
```	

#### #en CMD del Proyecto, Para acceder al panel administrativo de Django
```	
python manage.py createsuperuser
```	
#### #Ejecutar el servidor de desarrollo
```	
python manage.py runserver
```	

## Etapa 5: Creación de modelos en Django


#### #en CMD del Proyecto crear una nueva aplicación Django llamada blogsite
```	
python manage.py startapp blogsite
```	
#### #Estructura App 
```	
blogsite/
├── migrations/
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── tests.py
└── views.py
```	

#### Creando el modelo en blogsite/models.py
```	
from django.db import models
from django.utils.text import slugify
from django.urls import reverse  # Importar reverse para get_absolute_url

class Post(models.Model):
    title = models.CharField(max_length=255)  # Campo de texto corto para el título
    slug = models.SlugField(max_length=255, unique=True)  # URL amigable única
    content = models.TextField()  # Campo de texto largo para el contenido del post
    created_on = models.DateTimeField(auto_now_add=True)  # Fecha de creación automática
    author = models.CharField(max_length=100)  # Nombre del autor

    class Meta:
        ordering = ['-created_on']  # Orden descendente por fecha de creación

    def __str__(self):
        return self.title  # Representación legible del objeto (el título)

    def save(self, *args, **kwargs):
        if not self.slug:  # Si el slug está vacío, lo genera automáticamente
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)  # Llama al método original para guardar

    def get_absolute_url(self):
        """
        Genera la URL absoluta para un post específico.
        """
        return reverse('post_detail', args=[self.slug])
```	

## Etapa 6: Configuración de la aplicación y ejecución de migraciones

### 1. Registrar la aplicación blogsite en settings.py
Abre el archivo config/settings.py y localiza la lista INSTALLED_APPS. Agrega la aplicación blogsite para que Django la reconozca:
python
```	
INSTALLED_APPS = [
    # Aplicaciones predeterminadas de Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Nuestra aplicación
    'blogsite',
]
```	

#### ¿Qué hace esto?

Django necesita saber qué aplicaciones están activas en el proyecto. Al agregar blogsite, le indicamos que debe incluirla en el ciclo de vida del proyecto.

### 2. Crear las migraciones para el modelo
Ejecuta el siguiente comando en la consola CMD dentro del entorno virtual para generar las migraciones del modelo Post:
```	
python manage.py makemigrations

Salida esperada:
Migrations for 'blogsite':
  blogsite/migrations/0001_initial.py
    - Create model Post
```	

#### ¿Qué hace este comando?
Genera un archivo de migración (0001_initial.py) que contiene las instrucciones necesarias para crear la tabla blogsite_post en la base de datos.

#### Verifiquemos qué migraciones existen
```	
$ python manage.py showmigrations 

Salida esperada:
admin
[X] 0001_initial
[X] 0002_logentry_remove_auto_add
.........
```	

### 3. Aplicar las migraciones a la base de datos
Ejecuta el siguiente comando para aplicar las migraciones generadas:
```	
python manage.py migrate

Salida esperada:
Operations to perform:
  Apply all migrations: admin, auth, blogsite, contenttypes, sessions
Running migrations:
  Applying blogsite.0001_initial... OK
```	
#### ¿Qué hace este comando?
Ejecuta las instrucciones SQL definidas en las migraciones, creando la tabla blogsite_post y otros elementos relacionados en la base de datos PostgreSQL.

### 4. Verificar las tablas en PostgreSQL
Para confirmar que las tablas se han creado correctamente, accede a PostgreSQL desde tu terminal:
Abre la shell interactiva de PostgreSQL:
```	
psql -U userdjango -d project_orm_django
Lista las tablas disponibles:
sql
\dt
Salida esperada:
text
         List of relations
 Schema |      Name       | Type  | Owner
--------+-----------------+-------+---------
 public | blogsite_post   | table | userdjango
 ...
```	

#### ¿Dónde se define el nombre de la tabla?

__El nombre blogsite_post no se especifica directamente en el código del modelo. Django lo genera automáticamente basándose en:
El nombre de la aplicación: En este caso, blogsite.
El nombre del modelo: En este caso, Post.
Por defecto, Django usa esta convención para evitar conflictos entre tablas de diferentes aplicaciones.__

Ejemplo:
Si tienes una aplicación llamada blogsite y un modelo llamado Post, Django generará una tabla con el nombre blogsite_post


#### Verifica los campos de la tabla blogsite_post:
```	
psql
\d blogsite_post
Salida esperada:

                                  Table "public.blogsite_post"
   Column    |           Type           | Collation | Nullable |              Default              
-------------+--------------------------+-----------+----------+-----------------------------------
 id          | bigint                   |           | not null | generated by default as identity
 title       | character varying(255)   |           | not null |
 slug        | character varying(255)   |           | not null |
 content     | text                     |           | not null |
 created_on  | timestamp with time zone |           | not null |
 author      | text                     |           | not null |
Indexes:
    "blogsite_post_pkey" PRIMARY KEY, btree (id)
    "blogsite_post_slug_ad1b9573_like" btree (slug varchar_pattern_ops)
```	

#### ¿Qué hacen estos comandos?

* \dt: Lista todas las tablas disponibles en la base de datos.
* \d blogsite_post: Muestra los detalles de la estructura de la tabla, incluyendo columnas, tipos de datos e índices.

### 5. Probar el modelo desde el shell de Django
Abre el shell interactivo de Django para crear y consultar registros del modelo:

Abre el shell:
```	
python manage.py shell
#Importa el modelo y crea un nuevo post:

from blogsite.models import Post
post = Post(
    title="Mi primer post",
    content="Este es el contenido del post.",
    author="Admin"
)
post.save()

#Consulta todos los posts creados:
Post.objects.all()

Salida esperada:
<QuerySet [<Post: Mi primer post>]>
```	