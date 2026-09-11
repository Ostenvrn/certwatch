#!/usr/bin/env python3
"""
CertWatch — Мониторинг SSL-сертификатов
Использование:
    certwatch add <домен>       — добавить домен
    certwatch remove <домен>    — удалить домен
    certwatch list              — список доменов
    certwatch check             — проверить все домены
    certwatch check <домен>     — проверить один домен
"""
import sys
import os
import argparse
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from checkers.ssl_checker import SSLChecker
from storage.domain_store import DomainStore
from reporters.console_report import ConsoleReport


def cmd_add(args):
    store = DomainStore()
    store.add(args.domain)


def cmd_remove(args):
    store = DomainStore()
    store.remove(args.domain)


def cmd_list(args):
    store = DomainStore()
    domains = store.list_all()
    
    if not domains:
        print("📭 Список доменов пуст. Добавь: certwatch add example.com")
        return
    
    print(f"\n📋 Домены в мониторинге ({len(domains)}):")
    for i, d in enumerate(domains, 1):
        print(f"  {i}. {d}")
    print()


def cmd_check(args):
    store = DomainStore()
    checker = SSLChecker()
    
    # Если указан конкретный домен — проверяем только его
    if args.domain:
        domains = [store._normalize(args.domain)]
    else:
        domains = store.list_all()
    
    if not domains:
        print("📭 Список доменов пуст. Добавь: certwatch add example.com")
        return 1
    
    print(f"🔍 Проверяю {len(domains)} домен(ов)...\n")
    
    results = []
    for domain in domains:
        r = checker.check(domain)
        results.append(r)
    
    report = ConsoleReport(results)
    report.print()
    
    # Exit code для CI/CD
    has_problems = any(r["status"] in ("expired", "critical", "invalid") for r in results)
    return 1 if has_problems else 0


def main():
    parser = argparse.ArgumentParser(
        prog="certwatch",
        description="CertWatch — мониторинг SSL-сертификатов"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # add
    p_add = subparsers.add_parser("add", help="Добавить домен")
    p_add.add_argument("domain", help="Домен (например, example.com)")
    p_add.set_defaults(func=cmd_add)
    
    # remove
    p_remove = subparsers.add_parser("remove", help="Удалить домен")
    p_remove.add_argument("domain", help="Домен")
    p_remove.set_defaults(func=cmd_remove)
    
    # list
    p_list = subparsers.add_parser("list", help="Список доменов")
    p_list.set_defaults(func=cmd_list)
    
    # check
    p_check = subparsers.add_parser("check", help="Проверить сертификаты")
    p_check.add_argument("domain", nargs="?", help="Конкретный домен (опционально)")
    p_check.set_defaults(func=cmd_check)
    
    args = parser.parse_args()
    exit_code = args.func(args)
    sys.exit(exit_code or 0)


if __name__ == "__main__":
    main()
