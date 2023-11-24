from openai import AsyncOpenAI
from ..utils.setup import config


class ChatService:
    @staticmethod
    async def send_message(message: str) -> str:
        client = AsyncOpenAI(
            api_key=config.OPEN_API_KEY,
        )

        prompt = config.BASE_PROMPT + message

        try:
            stream = await client.chat.completions.create(
                messages=[{"role": "user", "content": prompt,}],
                model="gpt-3.5-turbo",
                temperature= 0.5,
                max_tokens=1024, 
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
            response = stream.choices[0].message.content
            return response.strip()
        except Exception:
            return "Pardon!"

        

        
