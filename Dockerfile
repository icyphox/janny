FROM python

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 

ENV JANNY_API_HOST="https://kubernetes.default"

RUN pip install poetry

COPY poetry.lock pyproject.toml /janny/
WORKDIR /janny
RUN poetry install --no-dev
COPY . ./
ENTRYPOINT ["python3", "-m","janny"]
