# django-rest-users
Basic endpoints of a REST API for the user application of the django framework.


La documentación detallada está en el directorio "docs".

Comienzo rápido
----------------

1. Agregar "rest_users" al setting INSTALLED_APPS::

      INSTALLED_APPS = (
          ...
          'rest_users',
      )

2. Incuir el URLconf de polls en el urls.py del proyecto::

      path('rest-users/', include('rest_users.urls')),

3. Correr `python manage.py syncdb` para crear los modelos de rest_users.

4. Levantar el servidor de desarrollo y visitar http://127.0.0.1:8000/

5. Visitar http://127.0.0.1:8000/rest-users/ para participar en una encuesta.

## License
[MIT](https://choosealicense.com/licenses/mit/)