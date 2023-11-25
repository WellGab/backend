from openai import AsyncOpenAI
from ..utils.setup import config
from ..models.chat import Conversations, Chats
from ..models.user import Users
import bson


class ChatModelService:
    @staticmethod
    def create_chat(user: Users, topic: str) -> tuple[str, str]:
        chat:  Chats = Chats(
            topic=topic,
            user=user
        ).save()
        return (str(chat.id), chat.topic)

    @staticmethod
    def update_chat(chat: Chats, new_topic: str = "", new_conversations: list[Conversations] = []) -> Chats:

        if new_topic != "":
            chat.topic = new_topic

        if len(new_conversations) > 0:
            chat.conversations.extend(new_conversations)

        chat.save()
        return chat

    @staticmethod
    def delete_chat(chat: Chats) -> bool:
        try:
            chat.delete()
            return True
        except Exception as e:
            # Handle specific exceptions if needed
            print(f"An error occurred while deleting the chat: {e}")
            return False

    @staticmethod
    def get_chat_by_id(id: str) -> Chats:
        chat = Chats.objects(id=bson.ObjectId(id)).first()
        return chat

    @staticmethod
    def get_chats_by_user(user: Users, page_number: int = 1, page_size: int = 50) -> list[Chats]:
        offset = page_size * (page_number - 1) or 0
        return Chats.objects(user=user).order_by('-created_at').limit(page_size).skip(offset)

    @staticmethod
    def get_user_chats_count(user: Users) -> int:
        return Chats.objects(user=user).count()


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
        Conversations(uid=bson.ObjectId(uid), message=message,
                      response=response).save()
