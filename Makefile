# Название виртуального окружения
VENV=venv

# Команды
.PHONY: init install run migrate clean

# Создание виртуального окружения и установка зависимостей
init:
	python -m venv $(VENV)
	. $(VENV)/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

# Установка зависимостей
install:
	. $(VENV)/bin/activate && pip install -r requirements.txt

# Запуск сервера разработки
run:
	. $(VENV)/bin/activate && uvicorn app.main:app --reload

# Инициализация базы данных
migrate:
	. $(VENV)/bin/activate && python -c "from app.core.database import Base, engine; Base.metadata.create_all(bind=engine)"

# Очистка (удаление базы и кэшей)
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -r {} +
	rm -f ./test.db

lint:
	. venv/bin/activate && pylint app/

mypy:
	. venv/bin/activate && mypy app/

