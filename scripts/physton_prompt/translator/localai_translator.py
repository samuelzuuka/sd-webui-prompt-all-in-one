from scripts.physton_prompt.translator.base_tanslator import BaseTranslator
import requests
import hashlib
import random
from scripts.physton_prompt.get_lang import get_lang


class LocalaiTranslator(BaseTranslator):
    def __init__(self):
        super().__init__('localai_free')

    def translate(self, text):
        if not text:
            return ''
        url = "http://localhost:9005/api/translate"
        # app_id = self.api_config.get('app_id', '')
        # app_secret = self.api_config.get('app_secret', '')
        # if not app_id:
        #     raise Exception(get_lang('is_required', {'0': 'APP ID'}))
        # if not app_secret:
        #     raise Exception(get_lang('is_required', {'0': 'APP Secret'}))
        # salt = random.randint(32768, 65536)
        send_text = text
        if isinstance(text, list):
            send_text = '\n'.join(send_text)
        # sign = app_id + send_text + str(salt) + app_secret
        # sign = hashlib.md5(sign.encode()).hexdigest()
        params = {
            'text': send_text,
            'from_lang': self.from_lang,
            'to_lang': self.to_lang,
        }
        response = requests.get(url, params=params, timeout=10)
        result = response.json()
        if not result or not result['success']:
            raise Exception('请求翻译接口失败!')
            if 'msg' in result:
                raise Exception(result['msg'])
        if 'data' not in result:
            raise Exception(get_lang('no_response_from', {'0': '本地AI翻译器'}))
        translated_text = []
        for item in result['data']:
            translated_text.append(item)
        if isinstance(text, list):
            return translated_text
        else:
            return '\n'.join(translated_text)

    def translate_batch(self, texts):
        if not texts:
            return []
        for text in texts:
            text = text.replace('\n', ' ')
        return self.translate(texts)
