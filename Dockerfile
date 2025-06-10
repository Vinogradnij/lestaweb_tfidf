FROM python:3.12.3-slim AS build
COPY requirements.txt .
RUN pip install --upgrade pip &&\
    pip install --user -r requirements.txt

FROM python:3.12.3-slim AS production
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
COPY --from=build /root/.local /root/.local
WORKDIR /app
RUN python -m nltk.downloader stopwords
COPY /src ./src
COPY /alembic ./alembic
COPY alembic.ini ./alembic.ini
CMD ["python", "src/main.py"]