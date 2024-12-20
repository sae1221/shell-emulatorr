# Shell Emulator 

Это простая эмуляция командной оболочки для работы с виртуальной файловой системой. В моём случае zip файл с каталогами.
Важно то что zip файл не распаковывается, все взаимодействие виртуальное.

**Функционал:**
Программа поддерживает базовые команды управления каталогами, такие как:
`ls` - осмотр папок,
`cd` - переход по директориям (cd .. - шаг назад),
`pwd` - выводит путь,
`mkdir` - создает папку,
`exit` - выходю

**Для работы программы потребуется::**
- Библиотека **py.yaml** для загрузки конфигурационного файла.

# Структура проекта

shell_emulator.py — основной файл с реализацией эмулятора оболочки.
config.yaml — конфигурационный файл, в котором указаны параметры, такие как путь к виртуальной файловой системе и файл лога.

log.csv — файл, в который записываются все действия пользователя.
![Alt text](https://github.com/sae1221/shell-emulatorr/blob/main/1.PNG)

fs.zip — архив с виртуальной файловой системой (например, файлы и каталоги).


# Запуск:

python shell_emulator.py

# Работа программы:
![Alt text](https://github.com/sae1221/shell-emulatorr/blob/main/2.PNG)
![Alt text](https://github.com/sae1221/shell-emulatorr/blob/main/3.PNG)

