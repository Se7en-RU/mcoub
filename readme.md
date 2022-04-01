# Coub Shazam searcher

Пакет ищет музыку с coub.com и  распознает ее с помощью Shazam

## Установка

    pip install shazamio flask[async] psycopg2
    sudo apt-get install ffmpeg libpq-dev

## Запуск

    export FLASK_ENV=production  
    export FLASK_APP=app.py  
    flusk run
    
## Роуты

      POST http://localhost:5000/search
      {url} - file url with song file

## БД

        create table coubs
        (
            id         	bigserial  primary key,
            coub_id     varchar(20) not null unique,
            shazam_data        jsonb not null,
            created_at timestamp NOT NULL DEFAULT NOW()
        );

        create index coubs_coub_id_index
            on coubs (coub_id);




