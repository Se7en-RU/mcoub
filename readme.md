# Coub Shazam music searcher

https://mcoub.com/

App provides search music from coub.com via Shazam.
Приложение осуществялет поиск музыки с coub.com посредством Shazam.

Webserver: Nginx + Gunicorn
Backend: Python + Flask
Frontend: Vue3


## Install | Установка
    docker-compose build
	cp services/nginx/nginx.conf.example services/nginx/nginx.conf
	cp backend/settings.ini.example backend/settings.ini
	cd frontend && npm run build

## Run | Запуск
    docker-compose up -d

# Frontend

http://localhost:3000/

# Backend Rest API

### Request | Запрос

`POST https://localhost/search/`

    curl -i -H 'Accept: application/json' -d '{"url":https://coub.com/view/3259pb"}'

### Response | Ответ

    {
        "data": {
            "coub": { ...data from coub.com... },
            "shazam": { ...data from shazam... },
        },
        "error": null
    }