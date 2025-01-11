# CHANGELOG


## v0.5.0 (2025-01-11)

### Features

- Health check
  ([`2f3f56f`](https://github.com/antonko/gigachat-adapter/commit/2f3f56f4322ef66caf6c8fe833d1334ffca5ee31))


## v0.4.1 (2025-01-08)

### Bug Fixes

- Исправлен ответ ошибки при stream-запросе
  ([`16ff682`](https://github.com/antonko/gigachat-adapter/commit/16ff6823bc36023781b96954331cb18ec1c215c3))

### Chores

- Конфигурация ruff
  ([`4d33b61`](https://github.com/antonko/gigachat-adapter/commit/4d33b611e3758af7fd35550e358729bff3b3dd55))

### Documentation

- Обновленный README.md
  ([`73accfe`](https://github.com/antonko/gigachat-adapter/commit/73accfe68bcc52275e988526009ffdc5541dafef))


## v0.4.0 (2025-01-07)

### Continuous Integration

- Github Action для проверки Pull Request
  ([`3b38d6f`](https://github.com/antonko/gigachat-adapter/commit/3b38d6f5e8a7ed8720682337a37fda11b1346989))

### Features

- Content в сообщениях как структура
  ([`c7edf18`](https://github.com/antonko/gigachat-adapter/commit/c7edf1887ffb6c69273ccc4000116e112789a740))

- Конфигурация логирование
  ([`df38bb4`](https://github.com/antonko/gigachat-adapter/commit/df38bb4098f6716a1eb7ac6cdc6a6e7e994ba188))

- Локальное сохранение хеша файла для исключения повторной загрузки в gigachat
  ([`6fca1c1`](https://github.com/antonko/gigachat-adapter/commit/6fca1c186ad64ba6718c7adcfb65b96a90024f9a))

- Реализована базовая работа с файлами в запросах чата
  ([`87acc42`](https://github.com/antonko/gigachat-adapter/commit/87acc428d61f79456e206fe3bc015ecd54bed719))


## v0.3.0 (2025-01-06)

### Chores

- Конфигурация для debug-запуска
  ([`23f74fb`](https://github.com/antonko/gigachat-adapter/commit/23f74fb2f59f886e26e91f501f1345cce7c23835))

### Features

- Формат ошибки (исключения) по схеме OpenAI API
  ([`be543f4`](https://github.com/antonko/gigachat-adapter/commit/be543f467ef4a685c603dbe8072416539a5915a9))

### Refactoring

- Рефакторинг структуры папок и файлов
  ([`1b639a2`](https://github.com/antonko/gigachat-adapter/commit/1b639a2d3d69b70681f2dc1046d6f01400685553))


## v0.2.4 (2025-01-06)

### Bug Fixes

- Корректное завершение ответа при stream (SSE)
  ([`add63f9`](https://github.com/antonko/gigachat-adapter/commit/add63f9b50a525b26033b137d8f1b100fd25859c))

### Documentation

- Обновлен README.md
  ([`3013ae3`](https://github.com/antonko/gigachat-adapter/commit/3013ae35bb56a84b1ea11212e155e62a5405d112))


## v0.2.3 (2025-01-05)

### Bug Fixes

- Публикация в Docker Hub
  ([`c9979b1`](https://github.com/antonko/gigachat-adapter/commit/c9979b1471c3001214d6c00cfa92c23bf99fca5e))


## v0.2.2 (2025-01-05)

### Bug Fixes

- Публикация в Docker Hub
  ([`a5b6640`](https://github.com/antonko/gigachat-adapter/commit/a5b6640067c95850d1e5a76bf24435af47965d62))


## v0.2.1 (2025-01-05)

### Bug Fixes

- Пояснение за monkey patch
  ([`9112b59`](https://github.com/antonko/gigachat-adapter/commit/9112b59e3dff6a2d5e470d2f6fb4c2d68220d9fe))

### Continuous Integration

- Исправлены ошибки публикации релиза
  ([`225684d`](https://github.com/antonko/gigachat-adapter/commit/225684db83f15611c867d7a692f4d004340bebda))

### Documentation

- Обновлен README.md
  ([`7180ab5`](https://github.com/antonko/gigachat-adapter/commit/7180ab5e9a3d14f6b964ee0481c03224591ebb49))

- Опечатки в README.md
  ([`6f915af`](https://github.com/antonko/gigachat-adapter/commit/6f915afc535f699d578f812d06f51ffbf65a46c2))


## v0.2.0 (2025-01-05)

### Bug Fixes

- Добавлена зависимость httpx с поддержкой http2
  ([`7980ba3`](https://github.com/antonko/gigachat-adapter/commit/7980ba369d67f40a0d10dce7c509601ffa838955))

- Изменение структуры проекта, папка models
  ([`5a6a061`](https://github.com/antonko/gigachat-adapter/commit/5a6a0613fa247bfe80aa70616d8bcc90b75ff955))

- Исправлено получение данных через stream
  ([`00b45a6`](https://github.com/antonko/gigachat-adapter/commit/00b45a65e72a436f697615c65e1375dfaaf3c461))

### Continuous Integration

- Версионирование и релизы
  ([`1b25990`](https://github.com/antonko/gigachat-adapter/commit/1b259907360790c33d6efb6a7fba6265340eeb38))

- Запуск github action под ubuntu-24.04
  ([`3fcb9cf`](https://github.com/antonko/gigachat-adapter/commit/3fcb9cf198e09d74c8e626828c03305ff1d0cfd5))

- Настроен ci/cd для публикации релизов
  ([`fbf90a5`](https://github.com/antonko/gigachat-adapter/commit/fbf90a5b2e6bd72cfd6cd66f94185a9ca655b3f0))

- Настройка github workflow
  ([`cd2194e`](https://github.com/antonko/gigachat-adapter/commit/cd2194e604417466523623813c0a37dcdd5419f9))

- Получение всех тегов и истории при формировании релиза
  ([`83b0c3d`](https://github.com/antonko/gigachat-adapter/commit/83b0c3de09f31fc30c93b574e4f083a5117f43f6))

- Создан Dockerfile
  ([`257b6f5`](https://github.com/antonko/gigachat-adapter/commit/257b6f5d26be8cc11e2584dfdb0236b98458c6b3))

### Documentation

- Красивый README.md
  ([`b24c2c0`](https://github.com/antonko/gigachat-adapter/commit/b24c2c08464754e0823d7a906db6ccb7c1ba05d6))

### Features

- Авторизация в endpoints и конфигурация приложения
  ([`a9f6c63`](https://github.com/antonko/gigachat-adapter/commit/a9f6c63032d6d3b2f8b8a2bdec43b882ba126137))

- Реализация stream в completions
  ([`c674d38`](https://github.com/antonko/gigachat-adapter/commit/c674d38df0ae886a681376b2d611f99b78fb2b83))

- Реализован метод completions в базовом варианте
  ([`bf1bb3c`](https://github.com/antonko/gigachat-adapter/commit/bf1bb3cabff92166b6555004275e37fce7049712))

- Реализован метод загрузки файлов
  ([`a4de3d9`](https://github.com/antonko/gigachat-adapter/commit/a4de3d96ce9f2f9de947a2ced56b4fcdc4298238))

- Создание приложения и первый работающий endpoint получения списка моделей
  ([`e0c5982`](https://github.com/antonko/gigachat-adapter/commit/e0c598245734d56ff52ac8feca9f8f2b170c1db1))

### Refactoring

- Изменены схемы списка моделей
  ([`09cf036`](https://github.com/antonko/gigachat-adapter/commit/09cf03685f7ea7fafa7e182ca3585c3886f7c8ad))


## v0.1.0 (2024-12-29)
