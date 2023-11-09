FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git cron

RUN git clone https://github.com/Gurriato/scrapping_oryx.git .

RUN pip install --no-cache-dir -r requirements.txt

ADD cron /etc/cron.d/cron

RUN chmod 0644 /etc/cron.d/tu-archivo-cron \
    && touch /var/log/cron.log

CMD cron && tail -f /var/log/cron.log
