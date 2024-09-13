import ipaddress
from django.conf import settings


def ipCheck(request):
    """ 
    Conseguimos la Direccion IP de quien se conecta a la APP 
    """
    
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()

    x_real_ip = request.META.get('HTTP_X_REAL_IP', '')
    if x_real_ip:
        return x_real_ip.strip()

    remote_addr = request.META.get('REMOTE_ADDR', '')
    if remote_addr:
        return remote_addr.strip()

    return '127.0.0.1'

class IPDebugMiddleware:
    """
    Middleware que habilita o deshabilita DEBUG basado en la IP de la solicitud.
    Soporta IPs individuales y rangos de IPs.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_ips = getattr(settings, 'DEBUG_ALLOWED_IPS', [])

    def __call__(self, request):
        #
        # Conseguimos IP del usuario
        ip = ipCheck(request)
        
        try:
            client_ip = ipaddress.ip_address(ip)
        except ValueError:
            client_ip = None
        
        # Establecemos estado Debug FALSE
        debug_state = False
        
        # Si IP Corresponde a las permitidas, DEBUG TRUE
        if any(self.is_ip_allowed(client_ip, allowed_ip) for allowed_ip in self.allowed_ips):
            settings.DEBUG = True
            debug_state = True
        
        # Intentamos informar al log Django del acceso a DEBUG
        if settings.DEBUG != debug_state:
            try:
                logger.info(f"DEBUG set to {debug_state} for IP {ip}")
            except:
                pass
        
        response = self.get_response(request)
        return response

    def is_ip_allowed(self, client_ip, allowed_ip):
        """
        Verifica si la IP del cliente está dentro del rango o es exacta.
        """
        try:
            allowed_network = ipaddress.ip_network(allowed_ip, strict=False)
            return client_ip in allowed_network
        except ValueError:
            return False
