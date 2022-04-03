# Coub Shazam music searcher

App provides search music from coub.com via Shazam.
Приоложение осуществялет поиск музыки с coub.com посредством Shazam.

## Install | Установка
    docker-compose build

## Run | Запуск
    docker-compose up -d

# Rest API

### Request | Запрос

`POST /search/`

    curl -i -H 'Accept: application/json' -d 'url=https://coub.com/view/30s87m' http://localhost:5000/search

### Response | Ответ

    {
        "data": {
            "coub": { ...data from coub.com... },
            "shazam": { ...data from shazam... },
        },
        "error": null
    }