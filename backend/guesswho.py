# coding=windows-1251

"""
����: ���� guess.txt ���������� ����� ��� ���������� 

(�������� �� http://www.biographyonline.net/people/famous-100.html ����� ����� �����)


�������� ���� "������ �� ����"

3 ������ ���������:
1) ������������ ����� ������ 1-10
2) ����� 1-50
3) ����� 1-100

- �� ������������ ���� �������� ������� ����
- ��������� ����� �������� � Google �� ���������� �����
- �������� ~30-50 ������ ������ �� ��������� �� ����� �����������
- ������� �������� �������� � �������� �� ������������ ��� ����������
  (����� ������� �� ����������� ������ ��������� ����)
- ����� ������ ������� ��������� ��� ���

�.�. ������� ��������� �����, �.�. ������ ������ � ������� �������� ��������� � ���-�������.

�.�. ��� ������ �������� ���������� ����������� ������� ���������������� ������ � Google
��� ����� ������������ � Google image search API
https://ajax.googleapis.com/ajax/services/search/images? ��� ��. ��������
�� � ������ API ����� ������������� ������������ ����������� �� ���-�� ��������
�.�. ���������� ���������� �� ������ ���������� ���-�� ����������� (����������)
�������� ��� ������ ������� �������� �����������. �.�. ���� �� ������ ����������� ����� N �������� (����������� API)


�.�. ���������� "��������������" ��������� ������ (�������� ������ ������ ����, 
������������ ������ ������ 1-30 ��������� � �.�.)
��� ����������� ���� ��� ��������� �������� �� ������������� �����

p.s. ����� � �������� ��� .zip (��� ������ �� github) ����� �������� �� isu.ifmo.ru

"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import sys
import requests
import random
from lxml import html
import json

IP = "127.0.0.1"
PORT = 8080

NAMES = []


def init_names() -> bool:
    NAMES.clear()
    try:
        file = open("names.txt", 'r')
        for name in file:
            NAMES.append(name.replace("\n", ""))
        file.close()
        print(NAMES)
        return True
    except IOError as io:
        print(f'error during names reading: {io}')
        return False


def get_four_names() -> []:
    arr = []
    i = 1
    while i < 5:
        next_name = random.choice(NAMES)
        if next_name not in arr:
            arr.append(next_name)
            i += 1
    return arr


def google_search() -> {}:
    names_arr = get_four_names()
    # todo: add parameter - search only face
    r = requests.get(f'https://www.google.com/search?tbm=isch&q={names_arr[0]} face')
    if r.status_code == 200:
        urls = []
        root = html.fromstring(r.text)
        for url in root.xpath('//img[@src]')[1:]:
            urls.append(url.attrib['src'])
        correct_name = names_arr[0]
        random.shuffle(names_arr)
        return {'status': r.status_code, 'url': random.choice(urls), 'correctName': correct_name,
                'names': names_arr, 'text': 'success'}
    else:
        return {'status': r.status_code, 'url': None, 'names': None, 'correctName': None, 'text': r.text}


class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        r = google_search()
        json_string = json.dumps(
            {'status': r.get('status'), 'text': r.get('text'), 'names': r.get('names'),
             'url': r.get('url'), 'correctName': r.get('correctName')})
        self.wfile.write(json_string.encode())


def run(server_class=HTTPServer, handler_class=Server):
    server_address = (IP, PORT)
    httpd = server_class(server_address, handler_class)

    print(f'server is up: see http://localhost:8080/')
    httpd.serve_forever()


if __name__ == '__main__':
    if init_names():
        run()
    else:
        print('Error during reading names')
        sys.exit(-1)
