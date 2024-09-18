# @Author: Bi Ying
# @Date:   2024-07-27 11:51:28
import time

from vectorvein.settings import settings
from vectorvein.types.enums import BackendType
from vectorvein.chat_clients import create_chat_client

from sample_settings import sample_settings

settings.load(sample_settings)
messages = [
    {
        "role": "user",
        "content": "节点名称是 FileLoader，FileLoader 节点连到 OCR 节点，使用 mermaid 语法表示流程图。直接开始补全，不要有任何解释。\n\n```mermaid\n",
    }
]


start_time = time.perf_counter()
client = create_chat_client(backend=BackendType.DeepSeek, model="deepseek-chat", stream=False)
response = client.create_completion(messages=messages, stop=["\n```"])
print(response)
end_time = time.perf_counter()
print(f"Stream time elapsed: {end_time - start_time} seconds")
