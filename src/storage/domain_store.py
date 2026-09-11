#!/usr/bin/env python3
"""Хранилище списка доменов для мониторинга"""
from pathlib import Path


class DomainStore:
    def __init__(self, data_file="data/domains.txt"):
        self.data_file = Path(data_file)
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.data_file.exists():
            self.data_file.touch()
    
    def add(self, domain):
        """Добавляет домен в список"""
        domain = self._normalize(domain)
        domains = self.list_all()
        
        if domain in domains:
            print(f"⚠️  Домен {domain} уже в списке")
            return False
        
        with open(self.data_file, 'a') as f:
            f.write(f"{domain}\n")
        print(f"✅ Добавлен: {domain}")
        return True
    
    def remove(self, domain):
        """Удаляет домен из списка"""
        domain = self._normalize(domain)
        domains = self.list_all()
        
        if domain not in domains:
            print(f"⚠️  Домен {domain} не найден")
            return False
        
        domains.remove(domain)
        with open(self.data_file, 'w') as f:
            f.write("\n".join(domains) + ("\n" if domains else ""))
        print(f"✅ Удалён: {domain}")
        return True
    
    def list_all(self):
        """Возвращает список всех доменов"""
        if not self.data_file.exists():
            return []
        
        with open(self.data_file, 'r') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    
    def _normalize(self, domain):
        """Убирает протокол, порт и пути из домена"""
        domain = domain.strip().lower()
        domain = domain.replace("https://", "").replace("http://", "")
        domain = domain.split("/")[0]
        domain = domain.split(":")[0]
        return domain
