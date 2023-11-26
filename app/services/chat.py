from openai import AsyncOpenAI
from ..utils.setup import config
from ..models.chat import Conversations, Chats, AnonConversations, AnonChats
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


class AnonChatModelService:
    @staticmethod
    def create_anon_chat(uid: str, topic: str) -> tuple[str, str]:
        chat:  AnonChats = AnonChats(
            topic=topic,
            uid=uid
        ).save()
        return (str(chat.id), chat.topic)

    @staticmethod
    def update_anon_chat(chat: AnonChats, new_topic: str = "", new_conversations: list[AnonConversations] = []) -> AnonChats:

        if new_topic != "":
            chat.topic = new_topic

        if len(new_conversations) > 0:
            chat.conversations.extend(new_conversations)

        chat.save()
        return chat

    @staticmethod
    def delete_anon_chat(chat: AnonChats) -> bool:
        try:
            chat.delete()
            return True
        except Exception as e:
            # Handle specific exceptions if needed
            print(f"An error occurred while deleting the chat: {e}")
            return False

    @staticmethod
    def get_anon_chat_by_id(id: str) -> AnonChats:
        chat = AnonChats.objects(id=bson.ObjectId(id)).first()
        return chat

    @staticmethod
    def get_anon_user_chats_count(uid: str) -> int:
        return AnonChats.objects(uid=uid).count()


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

    async def get_topic(message: str) -> str:
        client = AsyncOpenAI(
            api_key=config.OPEN_API_KEY,
        )

        prompt = "generate a topic for me from this: " + message

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
    async def interact(message: str, conversations: list[Conversations]) -> str:
        client = AsyncOpenAI(
            api_key=config.OPEN_API_KEY,
        )

        # convo = [
        #     {"role": "system", "content": config.BASE_PROMPT},
        # ]

        # count: int = 0
        # for c in conversations:
        #     count += 1
        #     if count == 1:
        #         convo = convo + [{"role": "user", "content": config.BASE_PROMPT + c.message},
        #                          {"role": "assistant", "content": c.reply},]
        #     else:
        #         convo = convo + [{"role": "user", "content": c.message},
        #                          {"role": "assistant", "content": c.reply},]

        # if len(conversations) < 0:
        #     message = config.BASE_PROMPT + message

        # convo = convo + [{"role": "user", "content": message},]

        prompt = config.BASE_PROMPT + message
        try:
            stream = await client.chat.completions.create(
                # messages=convo,
                messages=prompt,
                model="gpt-3.5-turbo",
                temperature=0.5,
                max_tokens=1024,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
            response = stream.choices[0].message.content
            # print("This is the response for: ", convo)
            print("This is the response for: ", response)
            print("This is the response for: ", response.strip())
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
