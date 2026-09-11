#!/usr/bin/env python3
"""Красивый вывод результатов проверки"""
try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    RED = Fore.RED; GREEN = Fore.GREEN; YELLOW = Fore.YELLOW
    CYAN = Fore.CYAN; MAGENTA = Fore.MAGENTA; RESET = Style.RESET_ALL
except ImportError:
    RED = GREEN = YELLOW = CYAN = MAGENTA = RESET = ""


STATUS_ICONS = {
    "ok":       f"{GREEN}🟢 OK{RESET}",
    "warning":  f"{YELLOW}🟡 СКОРО{RESET}",
    "critical": f"{RED}🔴 КРИТИЧНО{RESET}",
    "expired":  f"{RED}💀 ПРОСРОЧЕН{RESET}",
    "self_signed": f"{YELLOW}🔓 САМОПОДПИСАН{RESET}",
    "hostname_mismatch": f"{RED}🎭 НЕ СОВПАДАЕТ{RESET}",
    "invalid":  f"{RED}❌ НЕВАЛИДЕН{RESET}",
    "timeout":  f"{YELLOW}⏰ ТАЙМАУТ{RESET}",
    "dns_error":f"{RED}🌐 DNS ОШИБКА{RESET}",
    "refused":  f"{RED}🚫 ОТКАЗ{RESET}",
    "error":    f"{RED}⚠️  ОШИБКА{RESET}",
    "unknown":  f"{CYAN}❓ НЕИЗВЕСТНО{RESET}",
}


class ConsoleReport:
    def __init__(self, results):
        self.results = results
    
    def print(self):
        print(f"\n{MAGENTA}{'═' * 70}{RESET}")
        print(f"{MAGENTA}📜 CERT WATCH — Статус SSL-сертификатов{RESET}")
        print(f"{MAGENTA}{'═' * 70}{RESET}\n")
        
        # Заголовок таблицы
        header = f"{'ДОМЕН':<30} {'СТАТУС':<25} {'ИСТЕКАЕТ':<12} {'ОСТАЛОСЬ':<10} {'ИЗДАТЕЛЬ':<20}"
        print(f"{CYAN}{header}{RESET}")
        print(f"{CYAN}{'─' * 70}{RESET}")
        
        # Строки
        for r in self.results:
            domain = r["domain"][:28] + (".." if len(r["domain"]) > 28 else "")
            status = STATUS_ICONS.get(r["status"], "❓")
            
            if r["expires_at"]:
                expires = r["expires_at"].strftime("%Y-%m-%d")
                days = f"{r['days_left']} дн."
                if r['days_left'] < 0:
                    days = f"{abs(r['days_left'])} дн. назад"
            else:
                expires = "—"
                days = "—"
            
            issuer = (r["issuer"] or "—")[:18]
            
            # Учитываем ANSI-коды при выравнивании (приблизительно)
            print(f"{domain:<30} {status:<25} {expires:<12} {days:<10} {issuer:<20}")
        
        print(f"{MAGENTA}{'═' * 70}{RESET}\n")
        
        # Итоговая статистика
        self._print_summary()
    
    def _print_summary(self):
        stats = {
            "ok": 0, "warning": 0, "critical": 0, "expired": 0,
            "self_signed": 0, "hostname_mismatch": 0,
            "invalid": 0, "timeout": 0, "dns_error": 0, "refused": 0,
            "error": 0, "unknown": 0,
        }
        for r in self.results:
            stats[r["status"]] = stats.get(r["status"], 0) + 1
        
        print(f"{CYAN}📊 ИТОГО:{RESET}")
        print(f"  {GREEN}🟢 OK:{RESET}            {stats['ok']}")
        print(f"  {YELLOW}🟡 Скоро:{RESET}         {stats['warning']}")
        print(f"  {RED}🔴 Критично:{RESET}      {stats['critical']}")
        print(f"  {RED}💀 Просрочен:{RESET}     {stats['expired']}")
        print(f"  {YELLOW}🔓 Самоподписан:{RESET}  {stats['self_signed']}")
        print(f"  {RED}🎭 Не совпадает:{RESET}  {stats['hostname_mismatch']}")
        
        errors = (stats["invalid"] + stats["timeout"] + stats["dns_error"] 
                  + stats["refused"] + stats["error"])
        if errors:
            print(f"  {RED}⚠️  Ошибки:{RESET}        {errors}")
        
        print()
