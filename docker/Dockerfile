FROM python:3.12

WORKDIR /work

RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.8.2
ENV PATH="/root/.local/bin:$PATH"
RUN poetry config virtualenvs.create false

COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install

COPY . .

EXPOSE 8000

CMD python manage.py migrate && \
    python manage.py create_data && \ 
    uwsgi docker/uwsgi.ini --static-map /static=/work/static

