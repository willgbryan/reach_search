FROM python:3.11

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY backend .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=${OPENAI_API_KEY}
ENV SEARX_HOST="http://localhost:8080"

CMD ["python", "service.py"]