import requests
import json


class Translator:
    @staticmethod
    def _get_translate(text):
        url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?'
        key = 'trnsl.1.1.20190227T075339Z.1b02a9ab6d4a47cc.f37d50831b51374ee600fd6aa0259419fd7ecd97'
        lang = 'ru-en'
        r = requests.post(url, data={'key': key, 'text': text, 'lang': lang})
        return json.loads(r.text)['text'][0]
