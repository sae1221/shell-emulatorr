import os
import zipfile
import csv
from datetime import datetime
import yaml

class ShellEmulator:
    def __init__(self, config_file):
        self.load_config(config_file)
        self.current_dir = "/"
        self.virtual_fs = {"/": {"_files": []}}
        self.load_virtual_fs()
        self.setup_log_file()

    def load_config(self, config_file):
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
            self.hostname = config.get('hostname', 'unknown_host')
            self.fs_path = config.get('fs_path')
            self.log_path = config.get('log_path')
            if not self.fs_path or not self.log_path:
                raise ValueError("Отсутствуют обязательные поля в конфигурационном файле.")

    def setup_log_file(self):
        with open(self.log_path, 'w', newline='') as log_file:
            csv.writer(log_file).writerow(["время", "действие"])

    def log_action(self, action):
        with open(self.log_path, 'a', newline='') as log_file:
            csv.writer(log_file).writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), action])

    def load_virtual_fs(self):
        with zipfile.ZipFile(self.fs_path, 'r') as zf:
            for member in zf.infolist():
                parts = member.filename.strip('/').split('/')
                current_dir = self.virtual_fs["/"]
                for part in parts[:-1]:
                    current_dir = current_dir.setdefault(part, {"_files": []})
                if member.is_dir():
                    current_dir.setdefault(parts[-1], {"_files": []})
                else:
                    current_dir["_files"].append(parts[-1])

    def run(self):
        while True:
            command = input(f"{self.hostname}:{self.current_dir}$ ").strip()
            if command == "exit":
                self.log_action("exit")
                break
            elif command == "ls":
                self.ls()
            elif command == "pwd":
                self.pwd()
            elif command.startswith("cd"):
                self.cd(command)
            elif command.startswith("mkdir"):
                self.mkdir(command)
            else:
                print("Команда не найдена.")

    def ls(self):
        current_dir = self.navigate_to_dir(self.current_dir)
        if current_dir is not None:
            entries = [entry for entry in current_dir.keys() if entry != "_files"] + current_dir["_files"]
            print("\n".join(entries) if entries else "Нет файлов или директорий.")
        else:
            print(f"Ошибка: Директория '{self.current_dir}' не найдена.")
        self.log_action("ls")

    def pwd(self):
        print(self.current_dir)
        self.log_action("pwd")

    def cd(self, command):
        dir_name = command.split()[1] if len(command.split()) > 1 else None
        if dir_name == "..":
            self.current_dir = "/".join(self.current_dir.rstrip("/").split("/")[:-1]) or "/"
        elif dir_name:
            new_dir = f"{self.current_dir.rstrip('/')}/{dir_name}".strip('/')
            if self.navigate_to_dir(new_dir) is not None:
                self.current_dir = f"/{new_dir}".rstrip("/")
            else:
                print(f"Ошибка: Директория '{dir_name}' не найдена.")
        else:
            print("Использование: cd <директория>")
        self.log_action(f"cd {dir_name}")

    def mkdir(self, command):
        dir_name = command.split()[1] if len(command.split()) > 1 else None
        if not dir_name:
            print("Использование: mkdir <директория>")
            return
        current_dir = self.navigate_to_dir(self.current_dir)
        if current_dir is not None:
            if dir_name not in current_dir:
                current_dir[dir_name] = {"_files": []}
                print(f"Директория '{dir_name}' создана.")
                self.log_action(f"mkdir {dir_name}")
            else:
                print(f"Ошибка: Директория '{dir_name}' уже существует.")
        else:
            print("Ошибка: Неверная директория.")

    def navigate_to_dir(self, path):
        if path == "/":
            return self.virtual_fs["/"] 
        parts = path.strip('/').split('/')
        current_dir = self.virtual_fs["/"]
        for part in parts:
            if part in current_dir:
                current_dir = current_dir[part]
            else:
                return None
        return current_dir

if __name__ == "__main__":
    emulator = ShellEmulator("config.yaml")
    emulator.run()
