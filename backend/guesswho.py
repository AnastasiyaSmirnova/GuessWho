# coding=windows-1251

"""
Вход: файл guess.txt содержащий имена для угадывания 

(например из http://www.biographyonline.net/people/famous-100.html можно взять имена)


Написать игру "Угадай по фото"

3 уровня сложности:
1) используются имена только 1-10
2) имена 1-50
3) имена 1-100

- из используемых имен случайно выбрать одно
- запустить поиск картинок в Google по выбранному имени
- получить ~30-50 первых ссылок на найденные по имени изображения
- выбрать случайно картинку и показать ее пользователю для угадывания
  (можно выбрать из выпадающего списка вариантов имен)
- после выбора сказать Правильно или Нет

п.с. сделать серверную часть, т.е. клиент играет в обычном браузере обращаясь к веб-серверу.

п.с. для поиска картинок желательно эмулировать обычный пользовательский запрос к Google
или можно использовать и Google image search API
https://ajax.googleapis.com/ajax/services/search/images? или др. варианты
НО в случае API нужно предусмотреть существующие ограничения по кол-ву запросов
т.е. кешировать информацию на случай исчерпания кол-ва разрешенных (бесплатных)
запросов или другим образом обходить ограничение. Т.е. игра не должна прерываться после N запросов (ограничение API)


п.с. желательно "сбалансировать" параметры поиска (например искать только лица, 
использовать только первые 1-30 найденных и т.п.)
для минимизации того что найденная картинка не соответствует имени

p.s. Отчет и исходный код .zip (или ссылку на github) также высылать на isu.ifmo.ru

"""

import http.server
import socketserver
import requests
import random
from lxml import html
import json
import os

IP = "127.0.0.1"
PORT = 8080
Handler = http.server.SimpleHTTPRequestHandler

NAMES = []


def init_names() -> bool:
    NAMES.clear()
    try:
        file = open("names.txt", 'r')
        for name in file:
            NAMES.append(name)
        file.close()
        return True
    except IOError as io:
        print(f'error during names reading: {io}')
        return False


def google_search(name: str) -> json:
    r = requests.get(f'https://www.google.com/search?tbm=isch&q={name}')
    if r.status_code == 200:
        file_name = 'result.html'
        file = open(file_name, 'w+')
        file.write(r.text)
        file.close()
        # todo: process the errors (html error, parse error)

        urls = []
        # :( lxml can't https://
        root = html.parse(file_name).getroot()
        for url in root.xpath('//img[@src]')[1:]:
            urls.append(url.attrib['src'])

        os.remove(file_name)
        return json.dumps({'status': r.status_code, 'text': random.choice(urls)})
    else:
        return json.dumps({'status': r.status_code, 'text': r.text})


if __name__ == '__main__':
    init_names()
    res = google_search(random.choice(NAMES))
    print(res)

# with socketserver.TCPServer(("", PORT), Handler) as httpd:
#     if init_names():
#         print(f'server is up: see http://localhost:8080/')
#         httpd.serve_forever()
#     else:
#         sys.exit(-1)

"""
WHAT WE SHOULD DO? 

- user -> btn "start"
- server: get(/play) -> random name -> google(find images by name) -> RETURN??? (maybe links...) -> get 30, choose 1
- user: get 1 photo and 4 names (and 1 is correct), user play.

so only 1 request 

https://www.google.com/search?tbm=isch&q=findSomeImage -> result is html file, parse to get all <img SRC attr. 

I WANT BOOTSTRAP! to upgrade css 
"""
