from openai import OpenAI


class ChatService:
    @staticmethod
    def send_message(message: str) -> str:
        client = OpenAI(
            api_key='org-Zf5QvdNsItZESXSssUF77VRZ',
        )

        # chat_completions = client.chat.completions.create()
        # print("Reply: ", chat_completions)
        return f'Hello from GPT: {message}'
