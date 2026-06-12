FROM python:3.14-slim

RUN apt-get update && apt-get install -y \
    zsh curl cron \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY docker/entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

COPY docker/scheduler/crontab /etc/cron.d/lua-scheduler
RUN chmod 0644 /etc/cron.d/lua-scheduler

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["bash", "-c", "crontab /etc/cron.d/lua-scheduler && cron -f"]
