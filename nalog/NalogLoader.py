import requests
import json

class NalogLoader(object):
    def __init__(self):
        self.url = 'https://rmsp.nalog.ru/search-proc.json'
        self.headers = {}
        self.init_headers()

    def init_headers(self):
        self.headers.clear()
        self.headers['Host'] = 'rmsp.nalog.ru'
        self.headers['Connection'] = 'keep-alive'
        self.headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
        self.headers['X-Requested-With'] = 'XMLHttpRequest'
        self.headers['Origin'] = 'https://rmsp.nalog.ru'
        self.headers['Sec-Fetch-Site'] = 'same-origin'
        self.headers['Sec-Fetch-Mode'] = 'cors'
        self.headers['Sec-Fetch-Dest'] = 'empty'
        self.headers['Referer'] = 'https://rmsp.nalog.ru/index.html'
        self.headers['Accept-Encoding'] = 'gzip, deflate, br'
        self.headers['Accept-Language'] = 'ru,en;q=0.9'
        self.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 YaBrowser/21.8.2.381 Yowser/2.5 Safari/537.36'
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded'

    def download_n_parse(self, number):
        body = 'mode=quick&page=1&query={0}&pageSize=10&sortField=NAME_EX&sort=ASC'.format(number)
        response = requests.post(self.url, headers=self.headers, data=body)
        if response.status_code == 200:
            returned_data=json.loads(response.content.decode('utf-8'))
            for data in returned_data['data']:
                del(data['token'])
            return returned_data
        else:
            return None