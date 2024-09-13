# v0.1.5

import ipaddress
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def ipCheck(request):
    """
    Función mejorada para obtener la IP del visitante, asegurando que solo confiamos en proxies conocidos.
    (incluye soporte para CIDR)
    """

    # Lista de IPs atras del proxy
    trusted_proxies = getattr(settings, 'DEBUG_IP_TRUSTED_PROXIES', [])

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if x_forwarded_for:
        ip_list = [ip.strip() for ip in x_forwarded_for.split(',')]
        
        if ip_list:
            try:
                # Última IP en la cadena, correspondiente al proxy más cercano
                client_ip = ipaddress.ip_address(ip_list[-1])
            except ValueError:
                logger.error(f"Dirección IP no válida en X-Forwarded-For: {ip_list[-1]}")
                client_ip = None

            if client_ip:
                # Convertimos las IPs confiables a redes IP (incluye soporte para CIDR)
                trusted_networks = [ipaddress.ip_network(proxy, strict=False) for proxy in trusted_proxies if proxy]
                
                # Verificamos si la última IP (proxy más cercano) está en las redes confiables
                if any(client_ip in network for network in trusted_networks):
                    return ip_list[0]  # Devolvemos la primera IP (cliente original)
    

    x_real_ip = request.META.get('HTTP_X_REAL_IP', '')
    if x_real_ip:
        return x_real_ip.strip()


    remote_addr = request.META.get('REMOTE_ADDR', '')
    if remote_addr:
        return remote_addr.strip()

    return '8.8.8.8'

class IPDebugMiddleware:
    """
    Middleware que habilita o deshabilita DEBUG basado en la IP de la solicitud.
    Soporta IPs individuales y rangos de IPs.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_ips = getattr(settings, 'DEBUG_IP_ALLOWED', [])

    def __call__(self, request):

        # Si no esta habilitado, se cancela la carga de funciones
        if not getattr(settings, 'DEBUG_IP_ENABLED', False):
            return self.get_response(request)
        #
        # Conseguimos IP del usuario
        ip = ipCheck(request)
        
        try:
            client_ip = ipaddress.ip_address(ip)
        except ValueError:
            logger.error(f"Dirección IP inválida: {ip}")
            client_ip = None
        
        # Establecemos estado Debug FALSE
        debug_state = False
        
        # Si IP Corresponde a las permitidas, DEBUG TRUE
        if client_ip and any(self.is_ip_allowed(client_ip, allowed_ip) for allowed_ip in self.allowed_ips):
            settings.DEBUG = True
            debug_state = True
        else: 
            settings.DEBUG = False # Si viene de una IP no autorizada, se establece a FALSE
        
        # Intentamos informar al log Django del acceso a DEBUG
        if settings.DEBUG != debug_state:
            try:
                logger.info(f"DEBUG establecido a {debug_state} para la IP {ip}")
            except Exception as e:
                logger.error(f"Error al establecer DEBUG: {e}")
        
        response = self.get_response(request)
        return response


    def is_ip_allowed(self, client_ip, allowed_ip):
        """
        Verifica si la IP del cliente está dentro del rango o es exacta.
        Si `allowed_ip` es una IP individual, se asume una máscara de /32 o /128.
        """
        try:
            # Si es una IP individual (sin CIDR), la convertimos a /32 (IPv4) o /128 (IPv6)
            if '/' not in allowed_ip:
                allowed_ip += '/32' if ':' not in allowed_ip else '/128'
            
            allowed_network = ipaddress.ip_network(allowed_ip, strict=False)
            return client_ip in allowed_network
        except ValueError:
            logger.error(f"IP o red inválida en la configuración: {allowed_ip}")
            return False
