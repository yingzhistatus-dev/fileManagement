from openai import OpenAI

from utils.config import ARK_API_KEY, ARK_BASE_URL, ARK_MODEL


def generate_summary_with_doubao(content: str):
    if not content or not content.strip():
        return "摘要内容为空"

    if not ARK_API_KEY:
        raise ValueError("未配置 ARK_API_KEY，请先检查 backend/.env")

    if not ARK_MODEL:
        raise ValueError("未配置 ARK_MODEL，请先检查 backend/.env")

    client = OpenAI(
        api_key=ARK_API_KEY,
        base_url=ARK_BASE_URL,
    )

    user_prompt = f"""
请对下面的文本生成一个简洁、正式、适合业务演示的中文摘要。

要求：
1. 先给出“内容概述”
2. 再给出“关键信息”
3. 如内容较短，不要编造，按原文如实总结
4. 输出语言为中文
5. 结构清晰，便于在演示系统中直接展示

原文如下：
{content}
"""

    response = client.chat.completions.create(
        model=ARK_MODEL,
        messages=[
            {
                "role": "system",
                "content": "你是一个擅长文档理解与摘要生成的助手，输出要求准确、简洁、正式。"
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.3,
        max_tokens=800
    )

    result = response.choices[0].message.content
    return result.strip() if result else "摘要生成失败，未返回内容"