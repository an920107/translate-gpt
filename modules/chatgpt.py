from io import TextIOWrapper
import requests
from requests.auth import HTTPBasicAuth
import json
import re
import copy

class ChatGPT:

    def __init__(self, config_file: TextIOWrapper) -> None:
        self._config_dict = json.load(config_file)
        config_file.close()
        
    '''
    底下是讀入設定檔應有的 json 格式
    {
        "key": "", // ChatGPT API 密鑰.
        "prefix": "", // 前綴
        "suffix": "", // 後綴
        "config": { // 參閱 https://platform.openai.com/docs/guides/chat/introduction
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": ""
                }
            ]
        }
    }
    '''
    def post(self, text: str) -> str:

        URL = "https://api.openai.com/v1/chat/completions"

        to_post = copy.deepcopy(self._config_dict["config"])

        self._auth = HTTPBasicAuth("Bearer", self._config_dict["key"])

        to_post["messages"].append({
            "role": "user",
            "content": self._config_dict["prefix"] + text + self._config_dict["suffix"]
        })
        response = requests.post(URL, json=to_post, auth=self._auth)
        
        # print(self._config_dict["config"])
        # print(response.text)
        
        response_text = re.search(r"\"content\":\".*?\"", response.text).group()
        response_text = response_text[11:-1]
        response_text = re.sub(r"(\\n)+", "\n", response_text)
        response_text = re.sub(r"(\\\\n)+", "\n", response_text)

        if response_text[0] in ["，", "。", "！", "？"]:
            response_text = response_text[1:]

        return response_text