#!/usr/bin/env python3
"""Local Fortis supervisor. Ctrl+C stops only processes started here."""
import os
from pathlib import Path
import signal
import socket
import subprocess
import sys
import time
from urllib.error import URLError
from urllib.request import ProxyHandler, build_opener

ROOT = Path(__file__).resolve().parent.parent
HTTP = build_opener(ProxyHandler({}))


def healthy(url):
    try:
        with HTTP.open(url, timeout=2) as response:
            return response.status == 200
    except (URLError, TimeoutError, OSError):
        return False


def check_ports():
    for port in (3000, 8090):
        for family, host in ((socket.AF_INET, "127.0.0.1"), (socket.AF_INET6, "::1")):
            with socket.socket(family) as connection:
                connection.settimeout(0.3)
                if connection.connect_ex((host, port)) == 0:
                    raise RuntimeError(f"Порт {port} занят. Остановите прежний сервер; чужие процессы не завершаются.")


def stop(process):
    # The process may have exited while its descendants still hold a port.
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        pass
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    process.wait()


def wait_ready(process, url, timeout=90):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"Процесс завершился с кодом {process.returncode}; проверьте .fortis-dev/*.log")
        if healthy(url):
            return
        time.sleep(0.5)
    raise RuntimeError(f"Сервис не готов: {url}. Проверьте PostgreSQL и .fortis-dev/*.log")


def main():
    children = {}
    logs = []
    try:
        check_ports()
        if not (ROOT / "backend/.env").is_file():
            raise RuntimeError("Нужен backend/.env с настройками существующей локальной БД.")
        if not (ROOT / "frontend/node_modules/next").exists():
            raise RuntimeError("Сначала установите зависимости frontend: cd frontend && pnpm install")
        log_dir = ROOT / ".fortis-dev"
        log_dir.mkdir(exist_ok=True)
        env = dict(os.environ, FORTIS_RUNTIME_MODE="workspace", FORTIS_LOCAL_DEVELOPMENT="true",
                   BACKEND_URL="http://127.0.0.1:8090",
                   FORTIS_API_BASE_URL="http://127.0.0.1:8090",
                   NEXT_PUBLIC_FORTIS_API_BASE_URL="http://127.0.0.1:8090")
        services = {
            "backend": (["sh", "-c", "set -a; . ./.env; set +a; exec go run ./cmd/app/"],
                        ROOT / "backend", "http://127.0.0.1:8090/_/readiness"),
            "frontend": (["npm", "run", "dev", "--", "--hostname", "localhost", "--port", "3000"],
                         ROOT / "frontend", "http://localhost:3000/api/defense/projects?limit=1"),
        }

        def start(name):
            command, cwd, url = services[name]
            log = (log_dir / f"{name}.log").open("ab")
            logs.append(log)
            print(f"Запуск {name}… ({log.name})", flush=True)
            process = subprocess.Popen(command, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                                       stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
            children[name] = process
            wait_ready(process, url)
            print(f"{name}: готов", flush=True)

        for name in services:
            start(name)
        print("Fortis готов: http://localhost:3000 — Ctrl+C остановит оба сервера.", flush=True)
        retries = dict.fromkeys(services, 0)
        while True:
            for name, process in list(children.items()):
                if process.poll() is not None:
                    stop(process)
                    retries[name] += 1
                    if retries[name] > 3:
                        raise RuntimeError(f"{name}: три перезапуска не помогли; см. .fortis-dev/{name}.log")
                    print(f"{name} завершился; перезапуск {retries[name]}/3", flush=True)
                    time.sleep(1)
                    start(name)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nОстанавливаем Fortis…", flush=True)
        return 0
    except (RuntimeError, OSError) as error:
        print(f"Fortis: {error}", file=sys.stderr, flush=True)
        return 1
    finally:
        for process in reversed(list(children.values())):
            stop(process)
        for log in logs:
            log.close()


if __name__ == "__main__":
    def interrupt(*_):
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, interrupt)
    sys.exit(main())
