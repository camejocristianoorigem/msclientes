FROM python:3.14-rc-slim
WORKDIR /app
COPY requirements.txt .
COPY wheels /wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt
COPY . .
ENV PYTHONPATH=/app
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
