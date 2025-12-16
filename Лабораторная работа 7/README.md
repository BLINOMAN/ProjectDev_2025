# Лабораторная работа №4

Для проверки лабораторной необходимо установить библиотеки:

* pip install -r requirements.txt

После чего запустить последовательно команды:

* pytest
* pytest tests/test_models/ tests/test_repositories/ tests/test_services/
* pytest tests/test_routes/
* pytest --cov=app --cov-report=html
* pytest -n auto