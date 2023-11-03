FROM python:3.11-slim

RUN apt -y update && apt install -y curl wget ca-certificates gnupg
RUN mkdir -p /etc/apt/keyrings
RUN curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg

RUN echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list

RUN apt -y update && apt install nodejs -y
RUN npm install -g yukichant@3.1.0-beta.5

WORKDIR /app

RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv sync --dev

COPY ./server/app.py ./app.py
COPY ./server/static/ ./static

CMD ["pipenv", "run", "uvicorn", "app:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
