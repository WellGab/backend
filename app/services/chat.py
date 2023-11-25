from openai import AsyncOpenAI
from ..utils.setup import config
from ..models.chat import Conversations
import bson


class ChatService:
    @staticmethod
    async def send_message(message: str) -> str:
        client = AsyncOpenAI(
            api_key=config.OPEN_API_KEY,
        )

        prompt = config.BASE_PROMPT + message

        try:
            stream = await client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="gpt-3.5-turbo",
                temperature=0.5,
                max_tokens=1024,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
            response = stream.choices[0].message.content
            return response.strip()
        except Exception:
            return "Pardon!"

    @staticmethod
    def get_user_conversations(uid: str, page_number: int = 1, page_size: int = 50) -> list[Conversations]:
        offset = page_size * (page_number - 1) or 0
        return Conversations.objects(uid=bson.ObjectId(uid)).order_by('-created_at').limit(page_size).skip(offset)

    @staticmethod
    def get_user_conversations_count(uid: str) -> int:
        return Conversations.objects(uid=bson.ObjectId(uid)).count()
    
    @staticmethod
    def save_conversation(uid: str, message: str, response: str):
        Conversations(uid=bson.ObjectId(uid), message=message, response=response).save()
