from ..models.user import Subscribers
import bson


class SubscribeService:
    @staticmethod
    def subscriber_exists(email: str) -> bool:
        num_users = Subscribers.objects(email=email).count()
        return num_users > 0

    @staticmethod
    def create_subscriber(email: str) -> bool:

        subscriber: Subscribers = Subscribers(
            email=email
        ).save()
        id: str = str(subscriber.id)
        return subscriber.id != ""
