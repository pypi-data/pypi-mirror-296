#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : hanyuxinjie
# @Time         : 2024/9/18 13:30
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *

BASE_URL = 'https://xy.siliconflow.cn'

HTML_PARSER = re.compile(r'```html(.*?)```', re.DOTALL)


# s = """
# 这是一堆文本
# ```html
# 这是一段html
# ```
# 这是一堆文本
# """
#
# print(HTML_PARSER.findall(s))


async def create(
        text: str = '996',
        model: str = "Pro/THUDM/glm-4-9b-chat",
        stream: bool = True,
):
    """
    "Pro/THUDM/glm-4-9b-chat"
    "Qwen/Qwen2-Math-72B-Instruct"
    “deepseek-ai/DeepSeek-V2.5”
    """
    payload = {
        "messages": [
            {
                "role": "user",
                "content": text
            }
        ],
        # "chat_id": "i8yw46k",
        "model": model
    }
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=300) as client:
        async with client.stream(method="POST", url="/api/chat", json=payload) as response:
            content = ""
            async for chunk in response.aiter_lines():
                if stream:
                    # yield chunk.replace("智说新语", "汉语新解")
                    print(chunk, end="")
                # else:
                #     content += chunk

            # 非流
            # if content and (contents := HTML_PARSER.findall(content)):
            #     content = contents[0]
            # yield content
            # print(content)


if __name__ == '__main__':
    pass
    arun(create(text="火宝", model="Qwen/Qwen2-Math-72B-Instruct", stream=True))
    # arun(create(model="Qwen/Qwen2-Math-72B-Instruct", stream=True))
