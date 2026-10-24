# JenkinsQA_Python_2026_fall

Учебный проект для автоматизации браузерных тестов на **Python**, **Selenium**
и **pytest**, в том числе для тестирования Jenkins.

## Структура проекта

- `tests/` — тесты.
- `common/` — настройка окружения, работа с Jenkins, фильтрация и порядок тестов.
- `conftest.py` — общие фикстуры pytest, включая `browser` для работы с Jenkins.
- `requirements.txt` — Python-зависимости проекта.
- `.env.TEMPLATE` — шаблон локальных настроек.
- `.github/workflows/ci.yml` — запуск тестов в GitHub Actions.
- `.gitignore` — исключения для Git, включая локальный `.env`.

## Что нужно для запуска

- Python 3.12, как в CI.
- Google Chrome.
- Для тестов Jenkins — запущенный учебный экземпляр Jenkins и учётная запись
  с правами на создание и удаление тестовых данных.
- Доступ к интернету для установки зависимостей и загрузки драйвера браузера.

Фикстура `browser` перед тестами без зависимостей вызывает очистку Jenkins:
удаляет задания, представления, других пользователей, узлы и домены учётных
данных, сбрасывает ряд настроек. Используйте отдельный учебный Jenkins.

## Быстрый старт (Windows + PowerShell)

Выполняйте команды из корня проекта.

1. Создайте виртуальное окружение на Python 3.12:

   ```powershell
   py -3.12 -m venv .venv
   ```

2. Активируйте окружение:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

3. Установите зависимости:

   ```powershell
   python -m pip install -r requirements.txt
   ```

   `requirements.txt` содержит список пакетов, но сам по себе их не устанавливает.
   Версии пока не закреплены.

4. При первой настройке скопируйте шаблон:

   ```powershell
   Copy-Item .env.TEMPLATE .env
   ```

   Заполните `.env` адресом и учётными данными своего учебного Jenkins:

   ```dotenv
   JENKINS_USERNAME=<username>
   JENKINS_PASSWORD=<password>
   JENKINS_HOST=localhost
   JENKINS_PORT=8080
   BROWSER_NAME=chrome
   BROWSER_OPTIONS_CHROME=--window-size=1920,1080;--lang=en-US
   ```

   Вместо `JENKINS_HOST` и `JENKINS_PORT` можно задать `JENKINS_URL` с полным
   адресом Jenkins. Параметры Chrome разделяются точкой с запятой.
   Общая фикстура поддерживает Chrome. Локально оставьте `RUN_CI` незаданной:
   при `RUN_CI=true` загрузка `.env` отключается.

5. Убедитесь, что Jenkins доступен, и запустите тесты:

   ```powershell
   python -m pytest -v -s
   ```

Некоторые учебные тесты задают адреса сайтов и учётные данные прямо в коде;
настройки `.env` используются общими утилитами и фикстурой `browser`.

## Выбор тестов

Запуск одного файла:

```powershell
python -m pytest tests/test_Serj_Jenkins.py -v -s
```

Выбор тестов по части имени:

```powershell
python -m pytest -k jenkins -v -s
```

## CI

Workflow `.github/workflows/ci.yml` запускается для pull request в `main`.
Он устанавливает зависимости из `requirements.txt`, восстанавливает данные
Jenkins из `_jenkins_data/jenkins_backup*`, запускает Jenkins в Docker,
дожидается его готовности и выполняет pytest. Для общей фикстуры `browser`
передаются параметры Chrome с headless-режимом.
Для восстановления нужны файлы резервной копии, а в настройках репозитория —
секреты `ADMIN_USERNAME`, `ADMIN_PASSWORD`, `DOCKER_USERNAME`, `DOCKER_PASSWORD`.
В CI настройки передаются через переменные окружения.

## Возможные проблемы

- Если локальное окружение сообщает `No Python at ...`, пересоздайте его
  с установленным Python 3.12 и повторно установите зависимости.
- Если pytest сообщает `unrecognized arguments: --order-dependencies`,
  проверьте локальный `pytest.ini`: этот параметр относится к
  [плагину pytest-order](https://pytest-order.readthedocs.io/en/stable/configuration.html#order-dependencies),
  которого нет в `requirements.txt`. Для запуска с текущими зависимостями
  удалите этот параметр из `addopts` либо разово выполните
  `python -m pytest -o addopts="" -v -s`.
