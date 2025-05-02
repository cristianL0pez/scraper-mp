FROM python:3.9-slim

# Añade estas líneas al principio
ARG USER_ID=1000
ARG GROUP_ID=1000

WORKDIR /app

# Crea usuario y grupo con los mismos IDs que tu host
RUN groupadd -g ${GROUP_ID} appuser && \
    useradd -u ${USER_ID} -g appuser -s /bin/bash -m appuser && \
    chown appuser:appuser /app

# Continúa con el resto de tu Dockerfile original...
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    wget \
    curl \
    iputils-ping \
    chromium \
    chromium-driver && \
    rm -rf /var/lib/apt/lists/*


# Cambia a usuario no-root
USER appuser

# Resto de tu configuración...
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DISPLAY=:99

COPY --chown=appuser:appuser requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY --chown=appuser:appuser . .