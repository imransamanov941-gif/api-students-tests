# Тесты API Students

Автотесты для http://194.87.126.16/apidocs: операции со студентами (GET, POST, PUT, DELETE).

## Стек
Python, pytest, requests, allure-pytest

## Запуск
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pytest -v
```

После прогона результаты для Allure лежат в папке `allure-results`.
Просмотр отчёта (нужны Java и Allure CLI): `allure serve allure-results`

## Структура
- `api/client.py` клиент для запросов к API
- `tests/conftest.py` фикстуры, лог каждого теста прикрепляется к Allure
- `tests/test_students.py` тесты
- `config.py` адрес сервера

## Известные особенности сервера
Тесты с префиксом BUG в названии намеренно падают: они фиксируют найденные ошибки API.
Сервер ведёт себя нестабильно (данные то находятся, то нет), поэтому часть тестов использует повтор запроса.