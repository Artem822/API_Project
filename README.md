# Основное задание:

1. Account URL: http://localhost:8001/api/swagger/

2. Hospital URL: http://localhost:8002/api/swagger/

3. Timetable URL: http://localhost:8003/api/swagger/

4. Document URL: http://localhost:8004/api/swagger/

# Дополнительное задание:

1. ElasticSearch URL: http://localhost:9200/

2. Kibana URL: http://localhost:5601/

# Информация от участника

## Установка и запуск

Для установки и запуска приложения необходимо выполнить следующие шаги:

1. Установить Docker Desktop.
2. Клонировать репозиторий проекта.
3. Открыть папку с проектом в Visual Studio Code.
4. Запустить Docker Desktop.
5. Запустить контейнеры с помощью команды `docker-compose up -d` в терминале.
6. Дождаться полного создания и запуска всех контейнеров.

## Решения возможных проблем

- Перед запуском убедитесь, что у вас не заняты порты, используемые в `docker-compose.yml`.

- Если при запуске контейнеров, контейнер "Documents" не запустился нужно выполнить следующие шаги:
  1. Дождаться полного создания и запуска всех контейнеров.
  2. Перезапустить контейнер "Documents" командой `docker-compose restart documents`.
  3. Дождаться перезапуска контейнера "Documents".

