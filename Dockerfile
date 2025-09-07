FROM python:3.10

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install --no-install-recommends -y \
        build-essential \
        ca-certificates \
        git \
        gcc \
        libsqlite3-dev \
        libssl-dev \
        lsb-release \
        gpg-agent \
        wget 

RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor -o /usr/share/keyrings/postgresql-archive-keyring.gpg
RUN echo "deb [signed-by=/usr/share/keyrings/postgresql-archive-keyring.gpg] https://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" | tee /etc/apt/sources.list.d/pgdg.list
RUN apt-get update && apt-get install -y postgresql-16 \
        postgresql-server-dev-16 \
        postgresql-client-16 \
        libpq-dev

RUN git clone https://github.com/Rutvik-Trivedi/knowledge-llm.git
WORKDIR /knowledge-llm

RUN pip install -r requirements.txt
RUN su postgres -c psql -h localhost < scripts/db_setup.sql

RUN python3 -m spacy download en_core_web_sm
RUN python3 -m nltk.downloader punkt
RUN python3 -m nltk.downloader punkt_tab
RUN python3 manage.py migrate

EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]