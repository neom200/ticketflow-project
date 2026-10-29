import os

from openai import APIStatusError, APIConnectionError

from app.llm_client import get_client

client = get_client()

try:
    response = client.chat.completions.create(
        model=os.environ["OPENAI_MODEL"],
        messages=[
            {
                "role": "user",
                "content": "Responda apenas: conexão OK",
            }
        ],
        max_tokens=30,
    )

    print("Resposta:", response.choices[0].message.content)
    print("Tokens:", response.usage.total_tokens if response.usage else None)

except APIStatusError as e:
    print("Erro HTTP:", e.status_code)
    print("Detalhes:", e.response.text)

except APIConnectionError as e:
    print("Erro de conexão:", str(e))