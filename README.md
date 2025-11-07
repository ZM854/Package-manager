# Визуализатор графа зависимостей — Этап 1

## 1. Общее описание

На этом этапе реализуется минимальное CLI-приложение, которое принимает параметры из командной строки и проверяет их корректность.  
Пока что программа не анализирует зависимости — она только настраивается и выводит параметры в удобном виде.

## 2. Параметры запуска

- `--package` или `-p` — имя анализируемого пакета (обязательно).
- `--repo` или `-r` — URL-адрес репозитория (для `remote`) или путь к тестовому файлу (для `test`) (обязательно).
- `--mode` или `-m` — режим работы: `remote` (удалённый репозиторий) или `test` (локальный тестовый файл) (обязательно).
- `--filter` или `-f` — подстрока для фильтрации пакетов (необязательный параметр, пока не используется).

### Поведение параметров

- При режиме **`remote`** значение `--repo` должно быть корректным URL.
- При режиме **`test`** — существующим файлом.
- При ошибке выводится сообщение и программа завершается с ненулевым кодом.

### Формат вывода

При успешном запуске параметры выводятся построчно в формате `ключ=значение`:

```
package=ExamplePackage
repo=https://example.com
mode=remote
filter=test
```

---

## 3. Запуск программы

Требования: Python 3.13

### Примеры:

#### Удалённый режим

```
python main.py -p ExamplePackage -r https://example.com -m remote -f test
```

#### Тестовый режим

```
python main.py -p ExamplePackage -r ./data/test_repo.json -m test
```

---

## 4. Примеры ошибок

**Неверный URL (remote):**

```
Error: Invalid repository URL in remote mode.
```

**Несуществующий файл (test):**

```
Error: Invalid repository file path in test mode.
```

---

# Визуализатор графа зависимостей — Этап 2

## 1. Общее описание

На этом этапе реализована основная логика сбора данных о зависимостях пакета из NuGet-репозитория.
Приложение подключается к публичному package index `https://api.nuget.org/v3/index.json`, извлекает информацию о пакете и выводит его прямые зависимости.

---

## 2. Параметры запуска

Остались без изменений

## 3. Запуск программы

### Пример вызова для пакета Newtonsoft.Json:

```
python main.py -p Newtonsoft.Json -r https://api.nuget.org/v3/index.json -m remote
```

### Пример вывода

```
Analyzing package: Newtonsoft.Json
Mode: remote
Repository: https://api.nuget.org/v3/index.json
----------------------------------------
Connecting to NuGet repository: https://api.nuget.org/v3/index.json
Fetching package data: https://api.nuget.org/v3/registration5-semver1/newtonsoft.json/index.json
Direct dependencies:
- Microsoft.CSharp
- NETStandard.Library
- System.ComponentModel.TypeConverter
- System.Runtime.Serialization.Primitives
- Microsoft.CSharp
- NETStandard.Library
- System.ComponentModel.TypeConverter
- System.Runtime.Serialization.Formatters
- System.Runtime.Serialization.Primitives
- System.Xml.XmlDocument
```

## 4. Пример ошибок

**Некорректный URL (remote):**

```
Error: Invalid repository URL in remote mode.
```

**Ошибка при получении данных:**

```
Error fetching JSON from https://api.nuget.or/v3/index.json: <urlopen error [Errno 11001] getaddrinfo failed>
```
