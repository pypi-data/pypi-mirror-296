# Django IP Debug Middleware
![](https://img.shields.io/github/created-at/oguerrerog/django-ip-debug) ![](https://img.shields.io/github/last-commit/oguerrerog/django-ip-debug) ![](https://img.shields.io/github/stars/oguerrerog/django-ip-debug?style=flat-square)

**Middleware** para habilitar el modo **DEBUG** en Django **SOLO** para **ciertas IPs o rangos de IPs** correctamente ingresados en **settings.py**, útil para análisis o auditoría para despliegues de desarrollo y/o producción, evitando tener que modificar la configuración del proyecto cada vez que se necesite habilitar o deshabilitar el modo DEBUG. 
Esto permite a los desarrolladores y equipos de auditoría acceder a información de depuración detallada y resolver problemas de forma más eficiente, al mismo tiempo que se mantiene la seguridad del sitio web al restringir el acceso a esta información **solo a direcciones IP confiables**.

## Características
- Habilita o deshabilita el modo DEBUG según la IP del cliente.
- Soporta IPs individuales y rangos de IPs usando notación CIDR.
- Fácil integración con settings de Django.

## Requerimientos
- Django 3.0 o superior
- Python 3.0 o superior

## Instalación
1) Instala la librería desde pip:

```bash
pip install django-ip-debug

```
2) Agrega el la ruta del Middleware a tu archivo **settings.py**:

```python
MIDDLEWARE = [
    'ip_debug.middleware.IPDebugMiddleware',
    # Otros middlewares...
]
```

3) Define las IPs que pueden activar DEBUG a tu archivo **settings.py**:
(Opcionalmente, agrega rangos de IP con notación CIDR)
```python
DEBUG_ALLOWED_IPS = ['127.0.0.1', '192.168.0.50', '192.168.1.0/24']
```
## Logging
El middleware registra cada cambio en el estado de DEBUG, con la IP responsable del cambio.
No es requisito para funcionar, pero no esta de mas tener un registro. Si gustas, solo   asegúrate de configurar tu logger en **settings.py**:
```python
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'ip_debug': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}
```

## Versiones
0.1.0: Primer Commit
0.1.1: Se implementa función para detectar correctamente la dirección IP.
0.1.2: Corrección de Errores.


## Agradecimientos
Agradecimientos especiales a [MercadoPago](https://github.com/mercadopago "MercadoPago"), ese maravilloso y extraordinario servicio de pagos en línea que me "regalo" la emocionante oportunidad de enfrentarme a la "divertida" tarea de crear un entorno de producción/desarrollo solo para integrarme con ellos (es inevitable). Así que, lleno de "inspiración" (y tal vez un poco de desesperación), me lancé a la emocionante aventura de crear mi primer middleware para poder "debugear" mi proceso de integración y mantener mi cordura intacta ante la preocupación de tener el DEBUG disponible para todo el mundo.
Desde hoy dormiré en paz y sin despertar a medianoche, preocupado tratando de recordar si deje en el setting.py el debug en "**False**". xD