# django-rest-users
Basic endpoints of a REST API for the user application of the django framework.


La documentación detallada está en el directorio "docs".

## Comienzo rápido

* Agregar "rest_users" a la lista de INSTALLED_APPS del settings.py.

```python
INSTALLED_APPS = (
    ...,
    'rest_users',
)
```

* Incuir el URLconf de rest_users en el urls.py del proyecto:
```python
    path('rest-users/', include('rest_users.urls')),
```

* Correr `python manage.py migrate` para crear los modelos de rest_users.

* Levantar el servidor de desarrollo y visitar http://127.0.0.1:8000.

* Visitar http://127.0.0.1:8000/rest-users/ para ver los endpoints disponibles.


## License
[MIT](https://choosealicense.com/licenses/mit/)