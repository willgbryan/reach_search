FROM python:3.11

WORKDIR /usr/src/app

COPY backend/requirements.txt ./
COPY backend .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV OPENAI_API_KEY=""
ENV SEARX_HOST="http://localhost:8080"

CMD ["python", "-m", "backend.service"]