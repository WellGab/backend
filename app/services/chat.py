from openai import AsyncOpenAI
from ..utils.setup import config


class ChatService:
    @staticmethod
    async def send_message(message: str) -> str:
        client = AsyncOpenAI(
            api_key=config.OPEN_API_KEY,
        )

        prompt = config.BASE_PROMPT + message

        stream = await client.chat.completions.create(
            messages=[{"role": "assistant", "content": prompt,}],
            model="gpt-3.5-turbo",
            temperature= 0.5,
            max_tokens=1024, 
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stream=True
        )

        response = ""

        async for part in stream:
            content = part.choices[0].delta.content or ""
            response = f'{response}{content}'

        return response.strip()
