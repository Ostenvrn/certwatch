#!/usr/bin/env python3
"""SSL Checker — проверка срока действия сертификата"""
import socket
import ssl
from datetime import datetime, timezone
from dateutil import parser as date_parser


class SSLChecker:
    def __init__(self, timeout=10):
        self.timeout = timeout
    
    def check(self, domain, port=443):
        """
        Проверяет SSL-сертификат домена.
        Возвращает словарь с информацией или None при ошибке.
        """
        result = {
            "domain": domain,
            "port": port,
            "status": "unknown",
            "expires_at": None,
            "days_left": None,
            "issuer": None,
            "error": None,
        }
        
        try:
            # Получаем сертификат через ssl-соединение
            context = ssl.create_default_context()
            with socket.create_connection((domain, port), timeout=self.timeout) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
            
            # Парсим дату истечения
            expires_str = cert.get("notAfter")
            if expires_str:
                expires_at = date_parser.parse(expires_str).replace(tzinfo=timezone.utc)
                now = datetime.now(timezone.utc)
                days_left = (expires_at - now).days
                
                result["expires_at"] = expires_at
                result["days_left"] = days_left
                
                # Определяем статус
                if days_left < 0:
                    result["status"] = "expired"
                elif days_left <= 7:
                    result["status"] = "critical"
                elif days_left <= 30:
                    result["status"] = "warning"
                else:
                    result["status"] = "ok"
            
            # Извлекаем издателя
            issuer = cert.get("issuer", [])
            for item in issuer:
                for key, value in item:
                    if key == "organizationName":
                        result["issuer"] = value
                        break
        
        except ssl.SSLCertVerificationError as e:
            error_msg = str(e.verify_message).lower()
            
            if "expired" in error_msg or "has expired" in error_msg:
                result["status"] = "expired"
                result["error"] = "Сертификат просрочен"
            elif "self-signed" in error_msg or "self signed" in error_msg:
                result["status"] = "self_signed"
                result["error"] = "Самоподписанный сертификат (не доверенный)"
            elif "hostname" in error_msg or "doesn't match" in error_msg:
                result["status"] = "hostname_mismatch"
                result["error"] = "Имя домена не совпадает с сертификатом"
            else:
                result["status"] = "invalid"
                result["error"] = f"Сертификат невалиден: {e.verify_message}"
        
        except socket.timeout:
            result["status"] = "timeout"
            result["error"] = f"Таймаут подключения ({self.timeout} сек)"
        
        except socket.gaierror:
            result["status"] = "dns_error"
            result["error"] = "Не удалось разрешить DNS-имя"
        
        except ConnectionRefusedError:
            result["status"] = "refused"
            result["error"] = "Соединение отклонено (порт закрыт)"
        
        except Exception as e:
            result["status"] = "error"
            result["error"] = str(e)
        
        return result
