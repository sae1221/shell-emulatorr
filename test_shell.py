import unittest
from unittest.mock import patch, mock_open
import yaml
import os
import zipfile
import csv
from io import StringIO
from main import ShellEmulator

class TestShellEmulator(unittest.TestCase):
    def setUp(self):
        # Создание временного конфигурационного файла
        self.config_data = {
            'hostname': 'test_host',
            'fs_path': 'test_fs.zip',
            'log_path': 'test_log.csv'
        }
        self.config_content = yaml.dump(self.config_data)
        self.fs_content = {
            'virtual/': {},  # Создаем пустую виртуальную директорию
        }

        # Создание временной виртуальной файловой системы
        with zipfile.ZipFile(self.config_data['fs_path'], 'w') as zf:
            for path in self.fs_content:
                zf.writestr(path, '')  # Записываем пустые данные в виртуальную файловую систему

        # Создание конфигурационного файла
        with open('config.yaml', 'w') as config_file:
            config_file.write(self.config_content)

    def tearDown(self):
        os.remove('config.yaml')
        os.remove('test_fs.zip')
        if os.path.exists('test_log.csv'):
            os.remove('test_log.csv')

    # Тестируем команду 'ls'
    @patch('builtins.input', side_effect=['ls', 'cd virtual', 'ls', 'mkdir movies', 'ls', 'cd movies', 'pwd', 'exit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_shell_emulator_commands(self, mock_stdout, mock_input):
        emulator = ShellEmulator('config.yaml')
        emulator.run()

        # Проверка вывода программы
        output = mock_stdout.getvalue()

        expected_outputs = [
            "Нет файлов или директорий.",  # Ожидаем пустое содержимое директории 'virtual/'
            "Нет файлов или директорий.",  # Ожидаем пустое содержимое директории 'movies'
            "Директория 'movies' создана.",  # Проверяем создание директории 'movies'
            "movies",  # Ожидаем отображение текущей директории 'movies'
            "/virtual/movies"  # Ожидаем путь к директории 'movies'
        ]

        for expected in expected_outputs:
            self.assertIn(expected, output)

        # Проверка лога
        with open('test_log.csv', 'r') as log_file:
            log = list(csv.reader(log_file))

        actions = [row[1] for row in log[1:]]  # Пропускаем заголовок
        expected_actions = ['ls', 'cd virtual', 'ls', 'mkdir movies', 'ls', 'cd movies', 'pwd', 'exit']

        self.assertEqual(actions, expected_actions)  # Проверяем последовательность команд

if __name__ == '__main__':
    unittest.main()
