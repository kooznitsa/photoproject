FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /home/app

WORKDIR /home/app

COPY ../pyproject.toml ../poetry.lock* ./

RUN pip install poetry
RUN poetry install --no-root --no-interaction --no-ansi

COPY . ./

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
