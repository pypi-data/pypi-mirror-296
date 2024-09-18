# @Author: Bi Ying
# @Date:   2024-07-27 11:51:28
import time

import httpx
from vectorvein.settings import settings
from vectorvein.types.enums import BackendType
from vectorvein.chat_clients import create_chat_client

from sample_settings import sample_settings

settings.load(sample_settings)
messages = [
    {"role": "user", "content": "Please write quick sort code"},
]


start_time = time.perf_counter()
http_client = httpx.Client()
client = create_chat_client(backend=BackendType.DeepSeek, model="deepseek-chat", stream=False, http_client=http_client)
response = client.create_completion(messages=messages)
print(response)
end_time = time.perf_counter()
print(f"Stream time elapsed: {end_time - start_time} seconds")
