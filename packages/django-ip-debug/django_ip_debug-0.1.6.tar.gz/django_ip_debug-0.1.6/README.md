# Django IP Debug Middleware
![](https://img.shields.io/github/created-at/oguerrerog/django-ip-debug) ![](https://img.shields.io/github/last-commit/oguerrerog/django-ip-debug) ![](https://img.shields.io/github/stars/oguerrerog/django-ip-debug?style=flat-square)

**Middleware** que habilita el modo **DEBUG** en Django **EXCLUSIVAMENTE** a **ciertas IPs o rangos de IPs** definidos en **settings.py**, útil para análisis o auditoría para despliegues de desarrollo y/o producción de proyectos Django.

Esto evita la tarea de modificar la configuración del proyecto cada vez que se necesite habilitar o deshabilitar el modo DEBUG, lo que permite a los desarrolladores y equipos de auditoría o pruebas acceder a información de depuración detallada y resolver problemas de forma eficiente, al mismo tiempo que se mantiene la seguridad del sitio web al restringir el acceso a esta información **solo a direcciones IP confiables**.

## 🤓 Advertencia
Modificar el valor de DEBUG en tiempo de ejecución no es una práctica recomendada. DEBUG en Django está pensado para ser una configuración estática y se espera que su valor se establezca al inicio de la aplicación. Cambiarlo en tiempo de ejecución puede llevar a comportamientos inesperados.

Considerar el uso de esta herramienta solo para efectos de depuración, integraciones que necesiten un sitio en producción, testing, etc. 

## 🔎 Características
- Habilita o deshabilita el modo DEBUG según la IP del cliente.
- Soporta IPs individuales y rangos de IPs usando notación CIDR.
- Fácil integración con settings de Django.

## 💡 Requerimientos
- Django 4.2 o superior
- Python 3.9 o superior

## 📲 Instalación
1) Instala la librería desde pip:

```bash
pip install django-ip-debug
```

2) Agrega la ruta del Middleware a tu archivo **settings.py**:
```python
MIDDLEWARE = [
    'ip_debug.middleware.IPDebugMiddleware',
    # Otros middlewares...
]
```

3) Define las variables a tu archivo **settings.py**: 
```python
# Establecer DEBUG en False
DEBUG = False

# Habilita o deshabilita el middleware IPDebugMiddleware (django-ip-debug)
DEBUG_IP_ENABLED = True

# Lista de IPs Permitidas, puedes agregar rangos de IP con notación CIDR
DEBUG_IP_ALLOWED = ['127.0.0.1', '192.168.0.50', '192.168.1.0/24']

# Lista de Proxies autorizados, este ejemplo contiene la lista de Cloudflare
DEBUG_IP_TRUSTED_PROXIES = [
    '173.245.48.0/20',
    '103.21.244.0/22',
    '103.22.200.0/22',
    '103.31.4.0/22',
    '141.101.64.0/18',
    '108.162.192.0/18',
    '190.93.240.0/20',
    '188.114.96.0/20',
    '197.234.240.0/22',
    '198.41.128.0/17',
    '162.158.0.0/15',
    '104.16.0.0/13',
    '104.24.0.0/14',
    '172.64.0.0/13',
    '131.0.72.0/22'
]
```

## 📚 Versiones
- 0.1.0: Primer Commit
- 0.1.1: Se implementa función para detectar correctamente la dirección IP.
- 0.1.2: Corrección de Errores.
- 0.1.3: Mejoras Globales.
- 0.1.4: Mejoras para CIDR.
- 0.1.5: Fix setup.py
- 0.1.6: Fix URL setup.py

## 😜 Agradecimientos
Agradecimientos especiales a [MercadoPago](https://github.com/mercadopago "MercadoPago"), ese maravilloso y extraordinario servicio de pagos en línea que me "regalo" la emocionante oportunidad de enfrentarme a la "divertida" tarea de crear un entorno de producción/desarrollo solo para integrarme con ellos (es inevitable). Así que, lleno de "inspiración" (y tal vez un poco de desesperación), me lancé a la emocionante aventura de crear mi primer middleware para poder "debugear" mi proceso de integración y mantener mi cordura intacta ante la preocupación de tener el DEBUG disponible para todo el mundo.

Desde hoy dormiré en paz y sin despertar a medianoche preocupado tratando de recordar si deje en el setting.py el debug en "**False**". xD